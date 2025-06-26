#!/usr/bin/env python
"""
Always-works TFLite export by disabling the MLIR converter.
Outputs: models/model_f32.tflite
"""
import tensorflow as tf, pathlib

IN  = pathlib.Path("models/model.keras")
OUT = pathlib.Path("models/model_f32.tflite")

print("Loading Keras model…")
model = tf.keras.models.load_model(IN, compile=False)

print("Converting to TFLite (legacy converter)…")
conv = tf.lite.TFLiteConverter.from_keras_model(model)

# Force use of the V1 (non-MLIR) converter backend
conv.experimental_new_converter = False

# No optimizations (plain float32)
OUT.write_bytes(conv.convert())
print(f"✓ Saved {OUT} ({OUT.stat().st_size/1e6:.1f} MB)")
