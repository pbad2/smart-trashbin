#!/usr/bin/env python3
"""
Real-time image classification using TFLite and Picamera2 on Raspberry Pi.

Loads the TFLite model at models/model.tflite, captures frames via Picamera2,
performs inference to classify waste into one of four bins,
prints the class names, and routes hardware control via hardware_control.pick_bin().

Use `--debug` to display the video with overlaid predictions (press 'q' to quit).
"""
import time
import argparse
from pathlib import Path
import numpy as np
from picamera2 import Picamera2
import cv2
from tflite_runtime.interpreter import Interpreter as TFLiteInterpreter
from smartbin import SmartBin
import readchar

# Configuration
IMG_SIZE = 224
LABELS = Path("data/labels.txt").read_text().splitlines()

# Initialize interpreter
tflite_model_path = "models/model.tflite"
interpreter = TFLiteInterpreter(model_path=tflite_model_path)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
input_index = input_details[0]['index']
output_index = output_details[0]['index']
input_dtype = input_details[0]['dtype']


def show_info(text):
    print("\033[H\033[J", end='')  # clear terminal windows
    print(text)

# Camera setup using Picamera2
def open_camera():
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(
        main={"size": (IMG_SIZE, IMG_SIZE), "format": "RGB888"}
    )
    picam2.configure(config)
    picam2.start()
    print("[Info] Picamera2 started with 224x224 RGB output")
    return picam2

# Preprocessing (uint8 or float32 scaled to [-1,1])
def preprocess_image(img: np.ndarray) -> np.ndarray:
    if input_dtype == np.uint8:
        return img.astype(np.uint8)
    else:
        img_f32 = img.astype(np.float32)
        return (img_f32 / 127.5) - 1.0

# Prediction routine
def predict(frame: np.ndarray) -> tuple[int, int]:
    tensor = preprocess_image(frame)
    tensor = np.expand_dims(tensor, axis=0).astype(input_dtype)
    interpreter.set_tensor(input_index, tensor)
    interpreter.invoke()
    output = interpreter.get_tensor(output_index)[0]

    return int(np.argmax(output)), max(output)


# Main loop
def main(debug: bool = False):
    cam = open_camera()
    bin = SmartBin()
    try:
        while True:

            if True:
                while True:
                    frame = cam.capture_array()
                    cls_id, confidence = predict(frame)
                    cls_name = LABELS[cls_id]
                    cv2.putText(frame, cls_name + ", " + str(round(confidence, 5)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, .5 , (0,255,0), 2)
                    cv2.imshow("Classification", frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

            frame = cam.capture_array()
            cls_id, confidence = predict(frame)
            cls_name = LABELS[cls_id]
            print(f"Predicted: {cls_name}, confidence: {round(confidence, 2)}")
            
            is_full = bin.check_fullness()

            if is_full:
                return
            
            show_info("Press \n\t(c)ompost\n\t(e)lectronics\n\t(r)ecyclable\n\t(t)rash\n to open a partition")
            key = readchar.readkey()
            if key == "c":
                bin.open(0)
            elif key == "e":
                bin.open(1)
            elif key == "r":
                bin.open(2)
            elif key == "t":
                bin.open(3)
            
            #bin.open(cls_id)

            print("Press s to close the bin")
            while True:
                key = readchar.readkey()
                if key == "s":
                    bin.close_all()
                    break
            
    finally:
        cam.stop()
        if debug:
            cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true",
                        help="Display camera feed with overlay")
    args = parser.parse_args()
    main(debug=args.debug)

