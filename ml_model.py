import numpy as np
from keras.models import load_model
import joblib

# Load saved model
model = load_model("anemia_model.h5")

# Load label encoder
label_encoder = joblib.load("label_encoder.pkl")

def predict_anemia(features):
    features = np.array(features).reshape(1, -1)

    prediction = model.predict(features)

    predicted_class = prediction.argmax(axis=1)
    result = label_encoder.inverse_transform(predicted_class)

    return result[0]
