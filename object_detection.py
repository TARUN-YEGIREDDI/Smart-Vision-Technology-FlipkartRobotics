from ultralytics import YOLO
import cv2
import time

# Initialize the YOLO model
model = YOLO('Models/model2(18).pt')  # Replace with your actual model path

# Retrieve class names from the model
class_names = model.names  # Dictionary: {0: 'class0', 1: 'class1', ...}

# Initialize webcam (0 is usually the default camera)
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Optional: Set the desired frame width and height
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# To calculate FPS
prev_time = 0

print("Starting real-time object detection. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # Perform prediction on the current frame
    # The YOLO model expects images in RGB format
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = model.predict(rgb_frame, conf=0.25, verbose=False)

    # Process the results
    for result in results:
        # Extract bounding boxes, class labels, and confidence scores
        boxes = result.boxes.xyxy  # Bounding box coordinates in (x_min, y_min, x_max, y_max) format
        confidences = result.boxes.conf  # Confidence scores
        class_ids = result.boxes.cls  # Class labels (indices)

        # Iterate through each detected object
        for i in range(len(boxes)):
            x_min, y_min, x_max, y_max = map(int, boxes[i])  # Convert coordinates to integers
            confidence = confidences[i].item()  # Convert tensor to float
            class_id = int(class_ids[i].item())  # Convert tensor to int

            # Draw bounding box
            color = (0, 255, 0)  # Green color for the bounding box
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), color, 2)

            # Add a label with the class name and confidence
            label = f"{class_names[class_id]}: {confidence:.2f}"
            # Calculate text size to create a filled rectangle as background for text
            (text_width, text_height), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
            cv2.rectangle(frame, (x_min, y_min - text_height - baseline), 
                                 (x_min + text_width, y_min), color, -1)
            cv2.putText(frame, label, (x_min, y_min - baseline), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

            # Optional: Crop and save detected objects (can slow down processing)
            # cropped_img = frame[y_min:y_max, x_min:x_max]
            # cropped_img_filename = f"cropped_{class_names[class_id]}_{i}.jpg"
            # cv2.imwrite(cropped_img_filename, cropped_img)
            # print(f"Saved cropped image: {cropped_img_filename}")

    # Calculate and display FPS
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time) if prev_time else 0
    prev_time = curr_time
    cv2.putText(frame, f"FPS: {fps:.2f}", (20, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame with bounding boxes
    cv2.imshow('Real-Time Object Detection', frame)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exiting real-time object detection.")
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
