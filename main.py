import cv2
import numpy as np
# Replace 'your_video.mp4' with the path to your video file
video_path = 'Data/Cosmic Reef [1280 X 720].mp4'
cap = cv2.VideoCapture(video_path)

while True:
    # Read the next frame from the video
    ret, frame = cap.read()
    
    # Break the loop if we've reached the end of the video
    if not ret:
        break

    # Crop a 50x50 section from the frame (you can adjust the coordinates as needed)
    x, y, width, height = 100, 100, 50, 50
    cropped_section = frame[y:y+height, x:x+width]

    # Perform your analysis on the cropped section here
    # For example, you can apply image processing or computer vision algorithms

    # Display the original frame and the cropped section (for visualization purposes)
    cv2.imshow('Original Frame', frame)
    cv2.imshow('Cropped Section', cropped_section)

    # Break the loop if the user presses the 'q' key
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
