import cv2
import numpy as np
from ultralytics import YOLO


# Load the YOLOv8 model (e.g., YOLOv8n)
model = YOLO('yolov8n.pt')  # Use 'yolov8m.pt', 'yolov8l.pt', etc., for larger models

# Load an image
image_path = 'path/to/your/image.jpg'
image = cv2.imread(image_path)

# Perform object detection
results = model(image)

# Extract bounding boxes and visualize the results
for result in results:
    boxes = result.boxes  # Get the boxes
    for box in boxes:
        # Get the box coordinates, confidence, and class ID
        x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
        confidence = box.conf[0]  # Confidence score
        class_id = int(box.cls[0])  # Class ID

        # Draw the bounding box and label on the image
        label = f'Class: {class_id}, Confidence: {confidence:.2f}'
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Draw box
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

# Display the resulting image
cv2.imshow('Detected Objects', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
