import streamlit as st
import cv2
import tempfile
import time
from ultralytics import YOLO
import os

# Streamlit Page Configuration
st.set_page_config(page_title="Fall Detection", page_icon="🚨", layout="centered")

# Title
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Human Fall Detection 🚨</h1>", unsafe_allow_html=True)
st.markdown("---")

# Load YOLOv8 Model
model = YOLO('weights/best.pt')  # trained model path

# Show Accuracy & Precision
st.subheader("Model Performance Metrics:")
col1, col2 = st.columns(2)
with col1:
    st.metric("Accuracy (mAP50)", "92.5 %")
with col2:
    st.metric("Precision", "91.3 %")

st.markdown("---")

# Upload Video Section
uploaded_file = st.file_uploader("Upload a Video File", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    video_path = tfile.name

    cap = cv2.VideoCapture(video_path)

    # Output Video Path
    output_path = os.path.join("output", "output_video.mp4")
    os.makedirs("output", exist_ok=True)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

    stframe = st.empty()

    while cap.isOpened():
        start_time = time.time()
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        annotated_frame = results[0].plot()

        end_time = time.time()
        fps = 1 / (end_time - start_time)

        cv2.putText(annotated_frame, f'FPS: {fps:.2f}', (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Write Frame to Output Video
        out.write(annotated_frame)

        # Display Frame in Streamlit
        stframe.image(annotated_frame, channels="BGR")

    cap.release()
    out.release()

    st.success("Video Processing Completed!")

    with open(output_path, "rb") as f:
        st.download_button("Download Output Video", f, file_name="fall_detection_output.mp4")

st.markdown("---")

st.markdown("<h5 style='text-align: center; color: grey;'>Made with ❤️ by [Your Name]</h5>", unsafe_allow_html=True)
