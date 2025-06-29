import os
import cv2
import numpy as np
import requests
from ultralytics import YOLO

# Download the YOLOv8 model from the akanametov/yolo-face repository
model_url = "https://github.com/akanametov/yolo-face/releases/download/v0.0.0/yolov8n-face.pt"
model_path = "yolov8n-face.pt"

if not os.path.exists(model_path):
    print("Downloading YOLOv8 face model...")
    r = requests.get(model_url, allow_redirects=True)
    with open(model_path, 'wb') as f:
        f.write(r.content)
    print("Download complete.")

model = YOLO(model_path)

def blur_faces(image_path, output_path):
    """
    Detect faces in the image and apply a natural blur effect to them.

    Args:
        image_path (str): The path to the input image.
        output_path (str): The path to save the processed image.

    Returns:
        tuple: A tuple containing a boolean indicating success and the number of faces detected.
    """
    try:
        # Load the image
        img = cv2.imread(image_path)
        if img is None:
            return False, "Failed to read image"
        
        # Detect faces
        results = model(img)
        face_count = 0

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = [int(i) for i in box.xyxy[0]]
                w = x2 - x1
                h = y2 - y1
            
                # Calculate center and radius for circular mask
                center_x = x1 + w // 2
                center_y = y1 + h // 2
                radius = int(max(w, h) // 2 * 1.2)
                
                # Create circular mask
                mask = np.zeros(img.shape[:2], dtype=np.uint8)
                cv2.circle(mask, (center_x, center_y), radius, 255, -1)
                
                # Extract face region
                face_roi = cv2.bitwise_and(img, img, mask=mask)
                
                # Apply blur
                blurred_face = cv2.GaussianBlur(face_roi, (31, 31), 10)
                
                # Create inverted mask
                mask_inv = cv2.bitwise_not(mask)
                
                # Extract background
                background = cv2.bitwise_and(img, img, mask=mask_inv)
                
                # Combine background and blurred face
                img = cv2.add(background, blurred_face)
                face_count += 1
        
        # Save the result
        cv2.imwrite(output_path, img)
        return True, face_count
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return False, f"Error processing image: {str(e)}"

def process_video(video_path, output_path):
    """
    Detect faces in a video and apply a natural blur effect to them.

    Args:
        video_path (str): The path to the input video.
        output_path (str): The path to save the processed video.

    Returns:
        tuple: A tuple containing a boolean indicating success and a message.
    """
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return False, "Failed to open video"

        # Get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Create a temporary path for the frame
            temp_frame_path = "temp_frame.jpg"
            cv2.imwrite(temp_frame_path, frame)

            # Process the frame
            success, _ = blur_faces(temp_frame_path, temp_frame_path)
            if not success:
                print("Failed to process a frame.")
                continue

            # Read the processed frame and write to the output video
            processed_frame = cv2.imread(temp_frame_path)
            out.write(processed_frame)

        cap.release()
        out.release()
        os.remove("temp_frame.jpg")

        return True, "Video processed successfully."
    except Exception as e:
        print(f"Error processing video: {str(e)}")
        return False, f"Error processing video: {str(e)}"