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
        frame_skip = st.slider(
            "Frame skip (run model every N frames)",
            min_value=1, max_value=10, value=3,
            help="Higher = faster playback, fewer detections per second. 1 = every frame."
        )

        tfile = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded.name)[1])
        tfile.write(uploaded.read())
        tfile.close()

        cap = cv2.VideoCapture(tfile.name)
        frame_placeholder = st.empty()

        frame_count = 0
        last_annotated = None  # cache of most recent model output

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % frame_skip == 0:
                result = model.predict(frame, conf=0.25)[0]
                last_annotated = result.plot()

            if last_annotated is not None:
                frame_placeholder.image(last_annotated, channels="BGR", use_column_width=True)
            else:
                frame_placeholder.image(frame, channels="BGR", use_column_width=True)

            frame_count += 1

        cap.release()
        os.unlink(tfile.name)
