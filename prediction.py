from ultralytics import YOLO
import cv2

# Load the trained YOLO model
model = YOLO('Models/model2(18).pt')  # Replace with your actual model path

# Perform prediction on the input image
results = model.predict('output_image_with_boxes.jpg', conf=0.25)

# Load the original image using OpenCV
img = cv2.imread('output_image_with_boxes.jpg')

# Retrieve class names from the model
class_names = model.names  # Dictionary: {0: 'class0', 1: 'class1', ...}

# The results object contains the boxes, class labels, and confidence scores
for result in results:
    # Extract bounding boxes, class labels, and confidence scores
    boxes = result.boxes.xyxy  # Bounding box coordinates in (x_min, y_min, x_max, y_max) format
    confidences = result.boxes.conf  # Confidence scores
    class_ids = result.boxes.cls  # Class labels (indices)

    print(len(boxes))
    # Iterate through each detected object
    for i in range(len(boxes)):
        x_min, y_min, x_max, y_max = map(int, boxes[i])  # Convert coordinates to integers
        confidence = confidences[i].item()  # Convert tensor to float
        class_id = int(class_ids[i].item())  # Convert tensor to int

        # Draw bounding box
        color = (0, 255, 0)  # Green color for the bounding box
        cv2.rectangle(img, (x_min, y_min), (x_max, y_max), color, 2)

        # Add a label with the class name and confidence
        label = f"{class_names[class_id]}: {confidence:.2f}"
        # # Calculate text size to create a filled rectangle as background for text
        (text_width, text_height), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
        cv2.rectangle(img, (x_min, y_min - text_height - baseline), (x_min + text_width, y_min), color, -1)
        cv2.putText(img, label, (x_min, y_min - baseline), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

        # Crop the image using bounding box coordinates
        cropped_img = img[y_min:y_max, x_min:x_max]

        # Save or display the cropped image
        cropped_img_filename = f"cropped_{class_names[class_id]}_{i}.jpg"
        cv2.imwrite(cropped_img_filename, cropped_img)
        print(f"Saved cropped image: {cropped_img_filename}")

# Display the image with bounding boxes (Note: This may not work in some environments like Jupyter notebooks)
cv2.imshow('Image with Bounding Boxes', img)
cv2.waitKey(0)  # Wait for a key press to close the window
cv2.destroyAllWindows()

