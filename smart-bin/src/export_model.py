#!/usr/bin/env python
"""
Load the existing trained Keras model and export it as a TensorFlow SavedModel
and a TFLite flatbuffer, without retraining.
Run: python src/export_model.py
"""
import tensorflow as tf
from pathlib import Path

# Paths
KERAS_MODEL = Path("models/model.keras")
SAVED_MODEL_DIR = Path("models/saved_model")
TFLITE_OUT = Path("models/model.tflite")

print(f"Loading Keras model from {KERAS_MODEL} ...")
model = tf.keras.models.load_model(KERAS_MODEL, compile=False)

print(f"Exporting TensorFlow SavedModel to {SAVED_MODEL_DIR} ...")
# Keras 3 uses model.export() to create a SavedModel
model.export(str(SAVED_MODEL_DIR))

print(f"Converting SavedModel at {SAVED_MODEL_DIR} to TFLite flatbuffer ...")
converter = tf.lite.TFLiteConverter.from_saved_model(str(SAVED_MODEL_DIR))
tflite_model = converter.convert()
TFLITE_OUT.write_bytes(tflite_model)
print(f"✓ TFLite model saved to {TFLITE_OUT} ({TFLITE_OUT.stat().st_size/1e6:.1f} MB)")
