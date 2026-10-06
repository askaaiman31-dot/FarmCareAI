 import os
import numpy as np

from PIL import Image
from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf


app = Flask(__name__)
CORS(app)


# Load the trained AI model
MODEL_PATH = "farmcare_cnn.keras"

model = tf.keras.models.load_model(MODEL_PATH)


# PlantVillage class names
DATA_DIR = "raw/color"

class_names = sorted([
    name
    for name in os.listdir(DATA_DIR)
    if os.path.isdir(os.path.join(DATA_DIR, name))
])


@app.route("/")
def home():

    return jsonify({
        "message": "FarmCare AI backend is running!"
    })


@app.route("/predict", methods=["POST"])
def predict():

    if "image" not in request.files:

        return jsonify({
            "error": "No image uploaded"
        }), 400


    file = request.files["image"]


    image = Image.open(file).convert("RGB")

    image = image.resize((128, 128))


    image_array = np.array(
        image,
        dtype=np.float32
    )

    image_array = np.expand_dims(
        image_array,
        axis=0
    )


    predictions = model.predict(
        image_array,
        verbose=0
    )


    predicted_index = int(
        np.argmax(predictions[0])
    )


    predicted_class = class_names[
        predicted_index
    ]


    confidence = float(
        predictions[0][predicted_index] * 100
    )


    return jsonify({

        "disease": predicted_class,

        "confidence": round(
            confidence,
            2
        )

    })


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )