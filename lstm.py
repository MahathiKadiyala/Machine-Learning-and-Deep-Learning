# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 15:04:00 2026

@author: mahat
"""

############ LSTM on imdb

"""
Deeper LSTM on a built-in TensorFlow dataset (No custom functions/classes)
Task: Classify movie reviews as Positive or Negative
Dataset: IMDB (built into Keras, auto-downloads on first run)
Extra layers: second stacked LSTM, extra Dense layer, extra Dropout
"""

import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences

# STEP 1: Load the built-in dataset

vocab_size = 10000
(X_train, y_train), (X_test, y_test) = imdb.load_data(num_words=vocab_size)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))

# STEP 2: Pad sequences to the same length
max_length = 200
X_train = pad_sequences(X_train, maxlen=max_length)
X_test = pad_sequences(X_test, maxlen=max_length)

# STEP 3: Build the deeper LSTM model
model = models.Sequential([
    # Embedding: each word-integer becomes a learned 64-number vector
    layers.Embedding(input_dim=vocab_size, output_dim=64, input_length=max_length),

    # Dropout on word vectors so the model doesn't memorize specific words
    layers.Dropout(0.3),

    # EXTRA LAYER 1: first LSTM with return_sequences=True, so it passes
    # its output at every time step to the next LSTM (not just the last)
    layers.LSTM(64, return_sequences=True),

    # EXTRA LAYER 2: second LSTM builds higher-level patterns on top of
    # what the first LSTM found, then outputs one summary vector
    layers.LSTM(32),

    layers.Dropout(0.4),

    # EXTRA LAYER 3: additional Dense layer to refine the features
    layers.Dense(64, activation="relu"),
    layers.Dropout(0.3),

    layers.Dense(32, activation="relu"),

    # Output: one probability (0 = Negative, 1 = Positive)
    layers.Dense(1, activation="sigmoid")
])

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# STEP 4: Train the model
history = model.fit(
    X_train, y_train,
    validation_data=(X_test, y_test),
    epochs=4,
    batch_size=64
)

# STEP 5: Evaluate on the test set
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print("Test Accuracy:", test_accuracy)

# STEP 6: Predict on your own custom review
word_index = imdb.get_word_index()

review_text = "this movie was fantastic and the acting was brilliant"

encoded = [1]   # 1 = start-of-review token
for word in review_text.split():
    index = word_index.get(word, 2) # 2 = unknown word
    if index + 3 < vocab_size:
        encoded.append(index + 3)
    else:
        encoded.append(2)

new_review = pad_sequences([encoded], maxlen=max_length)

prediction = model.predict(new_review)[0][0]
label = "Positive" if prediction > 0.5 else "Negative"

print("Review:", review_text)
print("Prediction score:", prediction)
print("Predicted sentiment:", label)