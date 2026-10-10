import os
import json
import gdown
import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image

st.set_page_config(page_title="FarmCare AI", page_icon="🌱")

st.title("🌱 FarmCare AI")
st.write("Upload a plant leaf image to check for a possible disease.")

MODEL_PATH = "farmcare_cnn.keras"
CLASS_PATH = "class_names.json"
FILE_ID = "1VuSv_krLMZsecUh89TiXwsCYdDcetJ2N"

@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        url = f"https://drive.google.com/uc?id={FILE_ID}"
        gdown.download(url, MODEL_PATH, quiet=False)
    return tf.keras.models.load_model(MODEL_PATH)

@st.cache_data
def load_classes():
    with open(CLASS_PATH, "r") as f:
        return json.load(f)

try:
    model = load_model()
    class_names = load_classes()
except Exception as e:
    st.error(f"Unable to load model or class names: {e}")
    st.stop()

   
uploaded_file = st.file_uploader(
    "Choose a leaf image",
    type=["jpg", "jpeg", "png"],
    key="leaf_upload"
)


if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded leaf", use_container_width=True)

    if st.button("Analyze leaf"):
        image = image.resize((128, 128))
        image_array = np.array(image, dtype=np.float32)
        image_array = np.expand_dims(image_array, axis=0)

        with st.spinner("Analyzing leaf..."):
            predictions = model.predict(image_array, verbose=0)

        index = int(np.argmax(predictions[0]))

        if index < len(class_names):
            st.subheader("Prediction")
            st.write(
                class_names[index].replace("___", " — ").replace("_", " ")
            )
            st.write(f"Model confidence: {predictions[0][index] * 100:.2f}%")
            st.caption(
                "AI predictions can be wrong. Consult an agricultural expert "
                "before making treatment decisions."
            )
        else:
            st.error("The prediction does not match the class names file.")
