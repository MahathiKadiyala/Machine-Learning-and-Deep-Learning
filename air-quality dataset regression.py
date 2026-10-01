import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load dataset
df = pd.read_csv(
    r"C:\Users\mahat\Downloads\air+quality\AirQualityUCI.csv",
    sep=";",
    decimal=","
)

# Remove completely empty columns
df = df.dropna(axis=1, how="all")

# Replace -200 with NaN
df = df.replace(-200, np.nan)

# Convert columns to numeric wherever possible
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Check columns
print("Columns:")
print(df.columns)

# Target
y = df["CO(GT)"]

# Input features
X = df.drop(columns=["CO(GT)"])

# Keep only numeric columns
X = X.select_dtypes(include=["number"])

# Remove rows where target is missing
valid = y.notna()

X = X[valid]
y = y[valid]

# Fill missing values in X
imputer = SimpleImputer(strategy="mean")
X = imputer.fit_transform(X)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Linear Regression
model = LinearRegression()

model.fit(X_train, y_train)

# Prediction
y_pred = model.predict(X_test)

# Evaluation
print("\nLinear Regression Results")

print("MAE :", mean_absolute_error(y_test, y_pred))
print("MSE :", mean_squared_error(y_test, y_pred))
print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))
print("R2 Score:", r2_score(y_test, y_pred))
