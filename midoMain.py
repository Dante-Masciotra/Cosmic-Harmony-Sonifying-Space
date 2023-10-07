import cv2
import numpy as np
import mido
import time

# Create a virtual MIDI output port
output_port = mido.open_output('loopMIDI Port 1')  # Replace 'Virtual MIDI Port' with your desired port name

# MIDI note numbers for different colors
# You can adjust these note values as needed
RED_NOTE = 60  # C4
GREEN_NOTE = 62  # D4
BLUE_NOTE = 64  # E4

# Function to map color intensity to MIDI velocity
def map_intensity_to_velocity(intensity):
    return int(intensity * 127)

# Function to send a Program Change message to change the instrument
def change_instrument(program_number):
    output_port.send(mido.Message('program_change', program=program_number))

# Example: Change to instrument 20 (Church Organ)
change_instrument(20)

# Replace 'your_video.mp4' with the path to your video file
video_path = 'Data/Cosmic Reef [1280 X 720].mp4'
cap = cv2.VideoCapture(video_path)

while True:
    # Read the next frame from the video
    ret, frame = cap.read()

    if not ret:
        break

    # Crop a 50x50 section from the frame (you can adjust the coordinates as needed)
    x, y, width, height = 640, 360, 50, 50
    cropped_section = frame[y:y+height, x:x+width]

    # Get the average color intensity for each channel (R, G, B)
    avg_color = np.mean(cropped_section, axis=(0, 1))

    # Map color intensity to MIDI velocity
    red_velocity = map_intensity_to_velocity(avg_color[2] / 255.0)  # Red channel
    green_velocity = map_intensity_to_velocity(avg_color[1] / 255.0)  # Green channel
    blue_velocity = map_intensity_to_velocity(avg_color[0] / 255.0)  # Blue channel

    # Send MIDI notes based on color intensities
    output_port.send(mido.Message('note_on', note=RED_NOTE, velocity=red_velocity))
    output_port.send(mido.Message('note_on', note=GREEN_NOTE, velocity=green_velocity))
    output_port.send(mido.Message('note_on', note=BLUE_NOTE, velocity=blue_velocity))

    # Display the original frame and the cropped section (for visualization purposes)
    cv2.imshow('Original Frame', frame)
    cv2.imshow('Cropped Section', cropped_section)

    # Break the loop if the user presses the 'q' key
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()

# Release the virtual MIDI output port
output_port.close()
