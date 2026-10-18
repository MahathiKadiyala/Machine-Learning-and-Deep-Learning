# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 15:04:37 2026

@author: mahat
"""

##########lstm for regression
"""
Stock Price Prediction using LSTM (No custom functions/classes)
Task: Predict the next day's closing price from the previous 60 days
Dataset: External data downloaded from Yahoo Finance using yfinance
Install first (Colab):  !pip install yfinance
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from tensorflow.keras import layers, models

# STEP 1: Dataset
data = pd.read_csv(r"C:\Users\mahat\Downloads\stockmarketdata.csv")

print(data.head())
print("Total rows:", len(data))

# We only use the closing price for prediction
close_prices = data[["Close"]].values        # shape (days, 1)

# STEP 2: Scale the data (0 to 1)
# LSTMs train much better when values are small and similar in range.
# The scaler is fitted ONLY on the training part (first 80%) so the
# model never "peeks" at future prices.
train_size = int(0.8 * len(close_prices))

scaler = MinMaxScaler(feature_range=(0, 1))
scaler.fit(close_prices[:train_size])
scaled_data = scaler.transform(close_prices)

# STEP 3: Create windows (60 past days -> next day)
window_size = 60

X = []
y = []
for i in range(window_size, len(scaled_data)):
    X.append(scaled_data[i - window_size:i, 0])   # previous 60 prices
    y.append(scaled_data[i, 0])                   # the price right after

X = np.array(X)
y = np.array(y)

# LSTM expects (samples, time_steps, features)
X = X.reshape(X.shape[0], window_size, 1)

# Split by time (no shuffling): targets before train_size go to training
split = train_size - window_size
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

print("Training shape:", X_train.shape)
print("Testing shape:", X_test.shape)

# STEP 4: Build the LSTM model
model = models.Sequential([
    layers.LSTM(64, return_sequences=True, input_shape=(window_size, 1)),
    layers.Dropout(0.2),

    layers.LSTM(32),
    layers.Dropout(0.2),

    layers.Dense(16, activation="relu"),

    # Single output: the predicted (scaled) next-day price
    layers.Dense(1)
])

model.compile(optimizer="adam", loss="mean_squared_error")
model.summary()

# STEP 5: Train the model
history = model.fit(
    X_train, y_train,
    validation_data=(X_test, y_test),
    epochs=20,
    batch_size=32
)


# STEP 6: Predict on the test set and convert back to real prices


predicted_scaled = model.predict(X_test)

predicted_prices = scaler.inverse_transform(predicted_scaled)
actual_prices = scaler.inverse_transform(y_test.reshape(-1, 1))

rmse = np.sqrt(mean_squared_error(actual_prices, predicted_prices))
print("Test RMSE (in price units):", rmse)

# STEP 7: Plot actual vs predicted prices
plt.figure(figsize=(12, 6))
plt.plot(actual_prices, label="Actual Price")
plt.plot(predicted_prices, label="Predicted Price")
plt.title( " Stock Price Prediction using LSTM")
plt.xlabel("Days (test period)")
plt.ylabel("Price")
plt.legend()
plt.show()

# STEP 8: Predict the NEXT (unseen) day's price
last_60_days = scaled_data[-window_size:]                   # most recent 60 days
last_60_days = last_60_days.reshape(1, window_size, 1)

next_day_scaled = model.predict(last_60_days)
next_day_price = scaler.inverse_transform(next_day_scaled)

print("Predicted next trading day closing price:", next_day_price[0][0])