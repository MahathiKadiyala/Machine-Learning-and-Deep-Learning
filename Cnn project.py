# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 15:44:46 2026

@author: mahat
"""

# -*- coding: utf-8 -*-
"""
CNN Based Facial Emotion Detection
"""

import os
import warnings

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing.image import img_to_array

import cv2
import numpy as np

warnings.filterwarnings("ignore")


# ============================================================
# 1. DATASET PATH
# ============================================================

# Updated dataset folder
DATASET_DIR = r'C:\Users\mahat\OneDrive\Desktop\Machine_learning\happy'

# Check whether the dataset folder exists
if not os.path.exists(DATASET_DIR):
    print("Dataset folder not found!")
    print(DATASET_DIR)
    raise SystemExit

print("Dataset found at:")
print(DATASET_DIR)


# ============================================================
# 2. CHECK DATASET FOLDERS
# ============================================================

classes = ['angry', 'happy', 'neutral', 'sad', 'surprise']

print("\nChecking dataset folders...")

for class_name in classes:

    folder_path = os.path.join(DATASET_DIR, class_name)

    if os.path.exists(folder_path):
        files = os.listdir(folder_path)

        # Count image files
        image_files = [
            file
            for file in files
            if file.lower().endswith(('.jpg', '.jpeg', '.png'))
        ]

        print(class_name, "->", len(image_files), "images")

    else:
        print("ERROR: Folder not found ->", folder_path)


# ============================================================
# 3. IMAGE DATA GENERATOR
# ============================================================

batch_size = 16

train_datagen = ImageDataGenerator(
    rescale=1.0 / 255
)


# ============================================================
# 4. LOAD TRAINING IMAGES
# ============================================================

train_generator = train_datagen.flow_from_directory(
    DATASET_DIR,

    target_size=(48, 48),

    batch_size=batch_size,

    color_mode='grayscale',

    classes=classes,

    class_mode='categorical',

    shuffle=True
)


print("\nClass indices:")
print(train_generator.class_indices)

print("\nTotal training images:")
print(train_generator.n)


# ============================================================
# 5. BUILD CNN MODEL
# ============================================================

model = tf.keras.models.Sequential([

    # Input layer
    tf.keras.layers.Input(shape=(48, 48, 1)),

    # First convolution
    tf.keras.layers.Conv2D(
        64,
        (3, 3),
        activation='relu'
    ),

    tf.keras.layers.MaxPooling2D(
        pool_size=(2, 2)
    ),


    # Second convolution
    tf.keras.layers.Conv2D(
        64,
        (3, 3),
        activation='relu'
    ),

    tf.keras.layers.MaxPooling2D(
        pool_size=(2, 2)
    ),


    # Third convolution
    tf.keras.layers.Conv2D(
        64,
        (3, 3),
        activation='relu'
    ),

    tf.keras.layers.MaxPooling2D(
        pool_size=(2, 2)
    ),


    # Flatten
    tf.keras.layers.Flatten(),


    # Fully connected layer
    tf.keras.layers.Dense(
        64,
        activation='relu'
    ),


    # Output layer
    # 5 emotions
    tf.keras.layers.Dense(
        5,
        activation='softmax'
    )
])


# Display model
model.summary()


# ============================================================
# 6. COMPILE MODEL
# ============================================================

model.compile(
    loss='categorical_crossentropy',

    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.001
    ),

    metrics=['accuracy']
)


# ============================================================
# 7. TRAIN MODEL
# ============================================================

total_sample = train_generator.n

num_epochs = 5

steps_per_epoch = max(
    1,
    total_sample // batch_size
)


print("\nStarting training...")
print("Total images:", total_sample)
print("Batch size:", batch_size)
print("Epochs:", num_epochs)


history = model.fit(
    train_generator,

    steps_per_epoch=steps_per_epoch,

    epochs=num_epochs,

    verbose=1
)


# ============================================================
# 8. SAVE MODEL ARCHITECTURE
# ============================================================

model_json = model.to_json()

json_path = os.path.join(
    DATASET_DIR,
    "modelGG.json"
)

with open(json_path, "w") as json_file:
    json_file.write(model_json)


# ============================================================
# 9. SAVE MODEL WEIGHTS
# ============================================================

weights_path = os.path.join(
    DATASET_DIR,
    "model1GG.weights.h5"
)

model.save_weights(weights_path)


print("\n====================================")
print("Model saved successfully!")
print("JSON:", json_path)
print("Weights:", weights_path)
print("====================================")


# ============================================================
# 10. LOAD TRAINED MODEL
# ============================================================

print("\nLoading trained model...")

with open(json_path, "r") as json_file:
    loaded_model_json = json_file.read()


loaded_model = model_from_json(
    loaded_model_json
)


loaded_model.load_weights(
    weights_path
)


print("Loaded model successfully!")


# ============================================================
# 11. EMOTION LABELS
# ============================================================

class_labels = [
    'Angry',
    'Happy',
    'Neutral',
    'Sad',
    'Surprise'
]


# ============================================================
# 12. FACE DETECTOR
# ============================================================

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    'haarcascade_frontalface_default.xml'
)


# ============================================================
# 13. START WEBCAM
# ============================================================

cap = cv2.VideoCapture(0)


if not cap.isOpened():

    print("ERROR: Could not open webcam.")

    raise SystemExit


print("\nWebcam started.")
print("Press Q to quit.")


# ============================================================
# 14. REAL-TIME EMOTION DETECTION
# ============================================================

while True:

    # Capture frame
    ret, frame = cap.read()


    if not ret:

        print("Could not read webcam frame.")

        break


    # Convert frame to grayscale
    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )


    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )


    # Process every detected face
    for (x, y, w, h) in faces:

        # Draw rectangle around face
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (255, 0, 0),
            2
        )


        # Extract face
        roi_gray = gray[
            y:y + h,
            x:x + w
        ]


        # Resize to CNN input size
        roi_gray = cv2.resize(
            roi_gray,
            (48, 48),
            interpolation=cv2.INTER_AREA
        )


        # Check that image is not empty
        if np.sum(roi_gray) != 0:

            # Normalize pixels
            roi = roi_gray.astype('float32') / 255.0


            # Convert image to array
            roi = img_to_array(roi)


            # Add batch dimension
            roi = np.expand_dims(
                roi,
                axis=0
            )


            # Predict emotion
            preds = loaded_model.predict(
                roi,
                verbose=0
            )[0]


            # Find highest probability
            label_index = preds.argmax()


            # Get emotion name
            label = class_labels[label_index]


            # Get confidence
            confidence = preds[label_index] * 100


            # Text to display
            text = f"{label} {confidence:.1f}%"


            # Display emotion
            cv2.putText(
                frame,
                text,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )


    # Display webcam
    cv2.imshow(
        'Emotion Detector',
        frame
    )


    # Press Q to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):

        break


# ============================================================
# 15. RELEASE WEBCAM
# ============================================================

cap.release()

cv2.destroyAllWindows()

print("Emotion detector stopped.")