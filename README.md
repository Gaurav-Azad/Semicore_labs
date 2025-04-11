# 🚗 Semicore_lab Projects

This repository contains projects complete the  task of Semicore Labs 

---

# Task 1 - Real-Time Vehicle Detection and Parking Slot Monitoring

## Objective
Detect vehicles in real-time using YOLOv8 and monitor parking slot availability.

## Tools & Technologies Used
- Python
- OpenCV
- Ultralytics YOLOv8
- Numpy
- JSON (for parking slot coordinates)

## Directory Structure
```
Parking-Slot-Detection/
├── main.py               # Main Python script
├── coordinates.py        # For drawing polylines around the parking slot
├── parking_slots.json    # JSON file with parking slot coordinates
├── yolov8n.pt            # YOLOv8 Pre-trained model
|___output/                # Storing output video 
        └── output_parking_detection.mp4      
```

## Steps to Run

1. Clone the repository or copy the project files.

2. Install Dependencies:
```bash
pip install ultralytics opencv-python numpy
```

3. Prepare `parking_slots.json` with coordinates.py file for parking slots in the frame.
 Run the Code:
```bash
python coordinates.py
```

4. Run the Code:
```bash
python main.py
```

## Output
- Real-time vehicle detection with bounding boxes.
- Parking slot polylines drawn.
- Status of each parking slot displayed (Occupied / Empty).

---

# Task 3 - Human Fall Detection System 

## Objective
Detect Human Falls using custom YOLO model

---

## Status 
> Model is trained, Streamlit Web Application is developed for fall detection with video upload & download functionality.

---

## Tech Stack Used

- YOLOv8 (Ultralytics) for Fall Detection
- OpenCV for Video Processing
- Streamlit for Web App Interface
- Python for Backend Logic

---

## Directory Structure
```
human falling/
|── collab_training/     # Google Colab Training Notebook
|   └── train.ipynb
├── dataset/
|      └── test_video1.mp4
|       └── test_video2.mp4
├── output/              # Auto-generated Folder for Output Videos
│   └── output_video.mp4
|
├── weights/             # Trained YOLOv8 Model Weights
│   └── best.pt
|
├── detect.py            # Streamlit Web App Code

```

---

## Features (Implemented So Far)

- Upload any Video File (`.mp4`, `.avi`, `.mov`)
- Detect Human Falls in Real-Time
- Display FPS on Video
- Download Processed Output Video
- Display Accuracy & Precision of Trained Model
- Clean & Responsive Web Interface

---

## Model Performance

| Metric      | Value   |
|-------------|---------|
| Accuracy    | 92.5 %  |
| Precision   | 91.3 %  |

---

## How to Run the Fall Detection App

1. Clone the Repository:
```bash
git clone https://github.com/your-username/Fall-Detection-Project.git
cd Fall-Detection-Project
```

2. Install Required Packages:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit App:
```bash
streamlit run detect.py
```

---

## Note
> Task 2 is not done yet

---

## Developed By
> Made with ❤️ by Gaurav Kumar Azad 

---
