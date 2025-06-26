# #!/usr/bin/env python
# """
# Fine‑tune MobileNetV3‑Small for 4‑class classification.
# Outputs: models/model.h5
# Run: python src/train_model.py
# """
# import tensorflow as tf, os
# from pathlib import Path
# from tensorflow.keras import layers as L
# AUTOTUNE = tf.data.AUTOTUNE
# IMG_SIZE = 224
# BATCH = 32
# EPOCHS = 20
# data_dir = Path("data/images")

# train_ds = tf.keras.utils.image_dataset_from_directory(
#     data_dir, validation_split=0.2, subset="training",
#     seed=42, image_size=(IMG_SIZE, IMG_SIZE), batch_size=BATCH)

# val_ds = tf.keras.utils.image_dataset_from_directory(
#     data_dir, validation_split=0.2, subset="validation",
#     seed=42, image_size=(IMG_SIZE, IMG_SIZE), batch_size=BATCH)

# class_names = train_ds.class_names
# with open("data/labels.txt","w") as f: f.write("\n".join(class_names))

# train_ds = train_ds.cache().shuffle(1000).prefetch(AUTOTUNE)
# val_ds   = val_ds.cache().prefetch(AUTOTUNE)

# base = tf.keras.applications.MobileNetV3Small(
#         input_shape=(IMG_SIZE,IMG_SIZE,3), include_top=False,
#         weights="imagenet")
# base.trainable = False   # first phase

# inputs = L.Input(shape=(IMG_SIZE,IMG_SIZE,3))
# x = tf.keras.applications.mobilenet_v3.preprocess_input(inputs)
# x = base(x, training=False)
# x = L.GlobalAveragePooling2D()(x)
# x = L.Dropout(0.2)(x)
# outputs = L.Dense(len(class_names), activation='softmax')(x)
# model = tf.keras.Model(inputs, outputs)

# model.compile(optimizer=tf.keras.optimizers.Adam(1e-3),
#               loss="sparse_categorical_crossentropy",
#               metrics=["accuracy"])

# model.fit(train_ds, validation_data=val_ds, epochs=EPOCHS)
# base.trainable = True    # fine‑tune last blocks
# model.compile(optimizer=tf.keras.optimizers.Adam(1e-5),
#               loss="sparse_categorical_crossentropy",
#               metrics=["accuracy"])
# model.fit(train_ds, validation_data=val_ds, epochs=5)

# Path("models").mkdir(exist_ok=True)
# model.save("models/model.keras") 

#!/usr/bin/env python
"""
Fine‑tune MobileNetV3‑Small for 4‑class classification.
Outputs: models/model.keras and models/saved_model/
Run: python src/train_model.py
"""
import tensorflow as tf
from pathlib import Path
from tensorflow.keras import layers as L

# Constants
AUTOTUNE = tf.data.AUTOTUNE
IMG_SIZE = 224
BATCH = 32
EPOCHS = 20

data_dir = Path("data/images")

# Prepare datasets
train_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir, validation_split=0.2, subset="training",
    seed=42, image_size=(IMG_SIZE, IMG_SIZE), batch_size=BATCH)

val_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir, validation_split=0.2, subset="validation",
    seed=42, image_size=(IMG_SIZE, IMG_SIZE), batch_size=BATCH)

# Save class names
class_names = train_ds.class_names
Path("data").mkdir(exist_ok=True)
with open("data/labels.txt", "w") as f:
    f.write("\n".join(class_names))

# Optimize pipeline
train_ds = train_ds.cache().shuffle(1000).prefetch(AUTOTUNE)
val_ds = val_ds.cache().prefetch(AUTOTUNE)

# Build model
base = tf.keras.applications.MobileNetV3Small(
    input_shape=(IMG_SIZE, IMG_SIZE, 3), include_top=False, weights="imagenet")
base.trainable = False

inputs = L.Input(shape=(IMG_SIZE, IMG_SIZE, 3))
x = tf.keras.applications.mobilenet_v3.preprocess_input(inputs)
x = base(x, training=False)
x = L.GlobalAveragePooling2D()(x)
x = L.Dropout(0.2)(x)
outputs = L.Dense(len(class_names), activation='softmax')(x)
model = tf.keras.Model(inputs, outputs)

# Compile and train head
model.compile(
    optimizer=tf.keras.optimizers.Adam(1e-3),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)
model.fit(train_ds, validation_data=val_ds, epochs=EPOCHS)

# Fine‑tune last layers
base.trainable = True
model.compile(
    optimizer=tf.keras.optimizers.Adam(1e-5),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)
model.fit(train_ds, validation_data=val_ds, epochs=5)

# Save models
Path("models").mkdir(exist_ok=True)
# Keras native format
model.save("models/model.keras")
# TensorFlow SavedModel for TFLite conversion
model.save("models/saved_model", include_optimizer=False)
