import cv2
import json

# Resize Parameters
display_width = 1280  # You can change this as per your screen size

slots = []  # To store all slots
current_slot = []  # Temporary list to store current slot points

def click_event(event, x, y, flags, param):
    global current_slot, slots, img_resized, scale

    if event == cv2.EVENT_LBUTTONDOWN:
        # Scale back coordinates to original size
        x_original = int(x / scale)
        y_original = int(y / scale)

        current_slot.append((x_original, y_original))
        cv2.circle(img_resized, (x, y), 5, (0, 0, 255), -1)

        # Draw lines between clicked points
        if len(current_slot) > 1:
            cv2.line(img_resized, 
                     (int(current_slot[-2][0] * scale), int(current_slot[-2][1] * scale)),
                     (x, y), 
                     (255, 0, 0), 2)

        if len(current_slot) == 4:
            # Close the polygon
            cv2.line(img_resized, 
                     (x, y), 
                     (int(current_slot[0][0] * scale), int(current_slot[0][1] * scale)),
                     (255, 0, 0), 2)
            slots.append(current_slot)
            current_slot = []

        cv2.imshow("Select Parking Slots", img_resized)

# Load Original Image
img = cv2.imread("data/park1.png")
original_height, original_width = img.shape[:2]

# Calculate Resize Scale
scale = display_width / original_width
new_height = int(original_height * scale)
img_resized = cv2.resize(img.copy(), (display_width, new_height))

cv2.imshow("Select Parking Slots", img_resized)
cv2.setMouseCallback("Select Parking Slots", click_event)

print("Click 4 points per slot. Press 's' to save and 'q' to quit.")

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        with open("parking_slots.json", "w") as f:
            json.dump(slots, f, indent=4)
        print("Parking Slots Saved!")
    if key == ord('q'):
        break

cv2.destroyAllWindows()

