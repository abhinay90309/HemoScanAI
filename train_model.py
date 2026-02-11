import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical
import joblib

# Load dataset (put CSV in same folder)
df = pd.read_csv("diagnosed_cbc_data_v4.csv")

# Prepare data
y = df['Diagnosis']
X = df.drop(columns=["Diagnosis"])

print(X.columns)

le = LabelEncoder()
y = le.fit_transform(y)
y = to_categorical(y)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, train_size=0.75, random_state=43
)

# Build model
model = Sequential()
model.add(Dense(256, activation="relu", input_dim=len(X.columns)))
model.add(Dense(128, activation="relu"))
model.add(Dense(64, activation="relu"))
model.add(Dense(y.shape[1], activation="softmax"))

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# Train model
model.fit(X_train, y_train, epochs=20, batch_size=32)

# Save model
model.save("anemia_model.h5")
joblib.dump(le, "label_encoder.pkl")

print("Model trained and saved!")
