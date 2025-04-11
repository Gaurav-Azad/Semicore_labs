import cv2
import json
from ultralytics import YOLO
import numpy as np
import time

# Load Parking Slots from JSON
with open('parking_slots.json', 'r') as f:
    parking_slots = json.load(f)


# Load YOLOv8 Model
model = YOLO('yolov8n.pt')

# Load Video
cap = cv2.VideoCapture("data/video.mp4")

if not cap.isOpened():
    print("Error: Video not found or path is wrong!")
    exit()

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Initialize VideoWriter to Save Output Video
output_video = cv2.VideoWriter('output_parking_detection.mp4',
                               cv2.VideoWriter_fourcc(*'mp4v'),
                               fps,
                               (frame_width, frame_height))
slot_data = []
for _ in range(len(parking_slots)):
    slot_data.append({
        'current_status': False,
        'confirmed_status': 'Empty',
        'start_time': None
    })



while True:
    ret, frame = cap.read()

    if not ret:
        print("Video Ended or Cannot Read Frame")
        break

    empty_slots = 0
    occupied_slots = 0
    # Detect Cars
    results = model(frame)

    car_boxes = []

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            label = model.names[cls]

            if label == 'car':
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                car_boxes.append((x1, y1, x2, y2))

                # cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                # cv2.putText(frame, "Car", (x1, y1 - 10),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)


    current_time = time.time()
    for idx, slot in enumerate(parking_slots):
        slot_np = np.array(slot, np.int32).reshape((-1, 1, 2))
        
        # Reset current status
        slot_data[idx]['current_status'] = False
        
        # Check if any car is in this slot
        for (x1, y1, x2, y2) in car_boxes:
            car_center = ((x1 + x2) // 2, (y1 + y2) // 2)
            if cv2.pointPolygonTest(slot_np, car_center, False) >= 0:
                slot_data[idx]['current_status'] = True
                break

        # Update confirmed status based on 1-second rule
        if slot_data[idx]['current_status']:
            if slot_data[idx]['start_time'] is None:
                slot_data[idx]['start_time'] = current_time
            elif current_time - slot_data[idx]['start_time'] >=1:
                slot_data[idx]['confirmed_status'] = 'Occupied'
        else:
            slot_data[idx]['start_time'] = None
            slot_data[idx]['confirmed_status'] = 'Empty'

        # Update counters based on CONFIRMED status only
        if slot_data[idx]['confirmed_status'] == 'Occupied':
            occupied_slots += 1
            color = (0, 0, 255)  # Red
        else:
            empty_slots += 1
            color = (0, 255, 0)  # Green

        # Draw slot
        cv2.polylines(frame, [slot_np], True, color, 2)
        cv2.putText(frame, slot_data[idx]['confirmed_status'], 
                    tuple(slot[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)



        
    #counting slot in the frame    
    total_slot = len(parking_slots)
    cv2.putText(frame,f"Empty:{empty_slots}/{total_slot}",(10,30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8,(0,255,0),2)
    
    cv2.putText(frame,f"Occupied:{occupied_slots}/{total_slot}",(10,60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8,(0,0,255),2)
    

    # Show Video
    frame = cv2.resize(frame, (890, 540))
    cv2.imshow("Parking Slot Detection", frame)

    # Save Frame to Output Video
    output_video.write(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
# output_video.release()
cv2.destroyAllWindows()



