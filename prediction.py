from ultralytics import YOLO
import cv2

model = YOLO(r'Models\best.pt')

results = model.predict(r"C:\Users\darkn\Downloads\kur kur.jpg",conf = 0.25)

# print(results)



# Load the original image using OpenCV
img = cv2.imread(r"C:\Users\darkn\Downloads\kur kur.jpg")

# The results object contains the boxes, class labels, and confidence scores
for result in results:
    # Extract bounding boxes, class labels, and confidence scores
    boxes = result.boxes.xyxy  # Bounding box coordinates in (x_min, y_min, x_max, y_max) format
    confidences = result.boxes.conf  # Confidence scores
    class_ids = result.boxes.cls  # Class labels (optional if needed)

    # Iterate through each detected object
    for i in range(len(boxes)):
        x_min, y_min, x_max, y_max = map(int, boxes[i])  # Convert coordinates to integers
        confidence = confidences[i]  # Confidence score for the detection
        class_id = class_ids[i]  # Class label (optional)

        # Draw bounding box
        color = (0, 255, 0)  # Green color for the bounding box
        cv2.rectangle(img, (x_min, y_min), (x_max, y_max), color, 2)

        # Optionally, add a label with the class and confidence
        label = f"Class: {int(class_id)}, Conf: {confidence:.2f}"
        cv2.putText(img, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

# Show the image with bounding boxes
cv2.imshow('Image with Bounding Boxes', img)
cv2.waitKey(0)  # Wait for a key press to close the window
cv2.destroyAllWindows()

# Optionally, save the image with bounding boxes
cv2.imwrite('output_image_with_boxes.jpg', img)
