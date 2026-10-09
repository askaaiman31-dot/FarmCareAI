import json
import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image

st.set_page_config(
    page_title="FarmCare AI",
    page_icon="🌱",
    layout="centered"
)

MODEL_PATH = "farmcare_cnn (1).keras"
CLASS_PATH = "class_names (1).json"

@st.cache_resource
def load_model():
    return tf.keras.models.load_model(MODEL_PATH)

@st.cache_data
def load_classes():
    with open(CLASS_PATH, "r") as f:
        return json.load(f)

st.title("🌱 FarmCare AI")
st.write("Upload a plant leaf image to check for a possible disease.")

try:
    model = load_model()
    class_names = load_classes()
except Exception as e:
    st.error(f"Could not load the model or class names: {e}")
    st.stop()

uploaded_file = st.file_uploader(
    "Choose a leaf image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded leaf", use_container_width=True)

    if st.button("Analyze leaf"):
        with st.spinner("Analyzing image..."):
            image = image.resize((128, 128))
            image_array = np.array(image, dtype=np.float32) / 255.0
            image_array = np.expand_dims(image_array, axis=0)

            predictions = model.predict(image_array, verbose=0)
            predicted_index = int(np.argmax(predictions[0]))
            confidence = float(predictions[0][predicted_index] * 100)

        if predicted_index < len(class_names):
            st.subheader("Prediction")
            st.write(
                "Possible condition:",
                class_names[predicted_index].replace("___", " — ").replace("_", " ")
            )
            st.write(f"Model confidence: {confidence:.2f}%")
            st.caption(
                "This is an AI-generated estimate, not a confirmed diagnosis. "
                "Results can be incorrect; consult an agricultural expert if needed."
            )
        else:
            st.error("The model output does not match the class names file.")
