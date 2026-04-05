import os
import tempfile

import cv2
import numpy as np
import streamlit as st
from PIL import Image
from ultralytics import YOLO

st.set_page_config(page_title="Safety Helmet Detection", layout="wide")
st.title("Safety Helmet Detection")

@st.cache_resource
def load_model():
    return YOLO("models/yolov8s_ap.pt")

model = load_model()
mode = st.radio("Input type", ["Image", "Video"])

if mode == "Image":
    uploaded = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])
    if uploaded is not None:
        img = Image.open(uploaded).convert("RGB")
        img_np = np.array(img)
        result = model.predict(img_np, conf=0.25)[0]
        annotated = result.plot()
        st.image(annotated, channels="BGR", use_column_width=True)

else:
    uploaded = st.file_uploader("Upload video", type=["mp4", "avi", "mov"])
    if uploaded is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded.name)[1])
        tfile.write(uploaded.read())
        tfile.close()

        cap = cv2.VideoCapture(tfile.name)
        frame_placeholder = st.empty()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            result = model.predict(frame, conf=0.25)[0]
            annotated_frame = result.plot()
            frame_placeholder.image(annotated_frame, channels="BGR", use_column_width=True)

        cap.release()
        os.unlink(tfile.name)
