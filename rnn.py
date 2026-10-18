# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 14:42:10 2026

@author: mahat
"""

###########RNN on imdb dataset
 
"""
Task: Classify movie reviews as Positive or Negative (sentiment analysis)
Dataset: IMDB — a built-in default dataset in Keras (auto-downloads)
Extra layers: stacked SimpleRNN, Dropout, and an extra Dense layer
"""
 
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences
 
 
# STEP 1: Load the built-in IMDB dataset
vocab_size = 10000
 
(X_train, y_train), (X_test, y_test) = imdb.load_data(num_words=vocab_size)
 
print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))
 
 
# STEP 2: Pad sequences to the same length
max_length = 200
 
X_train = pad_sequences(X_train, maxlen=max_length)
X_test = pad_sequences(X_test, maxlen=max_length)
print("Padded training shape:", X_train.shape)
 
 
# STEP 3: Build a deeper RNN model
 
embedding_dim = 64
model = models.Sequential([
    # Embedding: turns each word-integer into a learned dense vector
    layers.Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_length),
 
    # Dropout right after embedding: randomly zeroes out some word
    # vectors during training, so the model doesn't over-rely on
    # specific words and generalizes better.
    layers.Dropout(0.3),
 
    # First SimpleRNN layer: return_sequences=True means it outputs
    # its hidden state at EVERY time step (not just the last one),
    # so the next RNN layer has a full sequence to read, not a
    # single summary vector.
    layers.SimpleRNN(64, return_sequences=True),
 
    # Second SimpleRNN layer: stacking RNNs like this lets the model
    # learn higher-level patterns on top of what the first RNN
    # already extracted (similar idea to stacking CNN layers).
    layers.SimpleRNN(32),
 
    # Extra Dense layer: adds more capacity to combine the RNN's
    # final features before making the decision.
    layers.Dense(32, activation="relu"),
    layers.Dropout(0.3),
 
    # Another Dense layer, smaller, refines the features further
    layers.Dense(16, activation="relu"),
 
    # Output layer: single probability (0=Negative, 1=Positive)
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
    epochs=5,
    batch_size=64
)
 
 
# STEP 5: Evaluate on the test set
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print("Test Accuracy:", test_accuracy)
 
 
# STEP 6: Predict on a new, unseen review
 
new_review = X_test[0:1]   # shape (1, max_length), already padded
 
prediction = model.predict(new_review)
predicted_label = "Positive" if prediction[0][0] > 0.5 else "Negative"
 
print("Raw prediction score (0=Negative, 1=Positive):", prediction[0][0])
print("Predicted sentiment:", predicted_label)
print("Actual sentiment:", "Positive" if y_test[0] == 1 else "Negative")