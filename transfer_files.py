# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 14:55:39 2026

@author: mahat
"""

########transfer learning
# -*- coding: utf-8 -*-
"""
Transfer Learning using MobileNetV2
"""

import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input


# =====================================================
# STEP 1: Dataset Directories
# =====================================================

dataset_dir = r'C:\Users\mahat\OneDrive\Desktop\Machine_learning\happy'

Angry_dir = os.path.join(dataset_dir, 'angry')
Happy_dir = os.path.join(dataset_dir, 'happy')
Neutral_dir = os.path.join(dataset_dir, 'neutral')
Sad_dir = os.path.join(dataset_dir, 'sad')
Surprise_dir = os.path.join(dataset_dir, 'surprise')


# Check sample files
train_Angry_names = os.listdir(Angry_dir)
print(train_Angry_names[:5])

train_Happy_names = os.listdir(Happy_dir)
print(train_Happy_names[:5])


# =====================================================
# STEP 2: Data Generator
# =====================================================

batch_size = 16

train_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input
)

target_size = (96, 96)


train_generator = train_datagen.flow_from_directory(

    dataset_dir,

    target_size=target_size,

    batch_size=batch_size,

    color_mode='rgb',

    classes=[
        'angry',
        'happy',
        'neutral',
        'sad',
        'surprise'
    ],

    class_mode='categorical',

    shuffle=True
)


print("Total images:", train_generator.n)
print("Class indices:", train_generator.class_indices)


# =====================================================
# STEP 3: Load MobileNetV2
# =====================================================

base_model = MobileNetV2(

    input_shape=(96, 96, 3),

    include_top=False,

    weights='imagenet'
)


# Freeze pretrained layers
base_model.trainable = False


# =====================================================
# STEP 4: Build Model
# =====================================================

inputs = tf.keras.layers.Input(
    shape=(96, 96, 3)
)

x = base_model(
    inputs,
    training=False
)

x = tf.keras.layers.GlobalAveragePooling2D()(x)

x = tf.keras.layers.Dense(
    64,
    activation='relu'
)(x)

x = tf.keras.layers.Dropout(
    0.3
)(x)

outputs = tf.keras.layers.Dense(
    5,
    activation='softmax'
)(x)


model = tf.keras.models.Model(
    inputs,
    outputs
)


# =====================================================
# STEP 5: Model Summary
# =====================================================

model.summary()


# =====================================================
# STEP 6: Compile
# =====================================================

model.compile(

    loss='categorical_crossentropy',

    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.001
    ),

    metrics=['accuracy']
)


# =====================================================
# STEP 7: Train
# =====================================================

num_epochs = 2

model.fit(

    train_generator,

    epochs=num_epochs,

    verbose=1
)


# =====================================================
# STEP 8: Save Model
# =====================================================

model_path = r'C:\Users\mahat\OneDrive\Desktop\Machine_learning\emotion_mobilenetv2.keras'

model.save(model_path)

print("\nTraining completed successfully!")

print("Model saved at:")
print(model_path)


import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load the trained model
model = load_model(r'C:\Users\mahat\OneDrive\Desktop\Machine_learning\emotion_mobilenetv2.keras')

# Class labels (same order as training)
class_labels = ['angry', 'happy', 'neutral', 'sad', 'surprise']

# Open webcam
cap = cv2.VideoCapture(0)  # 0 = default camera

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize to model input size
    img = cv2.resize(frame, (96, 96))
    img = np.expand_dims(img, axis=0)
    img = img.astype('float32')

    # Predict
    preds = model.predict(img)
    emotion = class_labels[np.argmax(preds)]

    # Show prediction on frame
    cv2.putText(frame, emotion, (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Emotion Detection', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
