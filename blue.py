import cv2
import numpy as np
import mido
from mido import MidiFile, MidiTrack, Message
import matplotlib.pyplot as plt

# Read the list of average colors from the text file
average_colors = []
with open('average_colors.txt', 'r') as file:
    for line in file:
        # Split the line into individual RGB values and convert them to integers
        r, g, b = map(int, line.strip('[]\n').split())
        color = np.array([r, g, b])
        average_colors.append(color)

# Create a MIDI file
midi_file = MidiFile()
track = MidiTrack()
midi_file.tracks.append(track)

# Define MIDI note numbers corresponding to the desired pitch range
min_note = 60  # MIDI note number for C4
max_note = 96  # MIDI note number for C7

# Initialize variables to track the current note and its duration
current_note = None
current_duration = 0

# Normalize the blue channel values to the range [0, 1] and map them to MIDI notes
for color in average_colors:
    blue_normalized = color[2] / 255.0  # Normalize blue channel
    note = int(min_note + (max_note - min_note) * blue_normalized)
    velocity = 64  # Set the velocity (volume) of the note

    # Check if the note has changed
    if note != current_note:
        # If the note has changed, add a note-off message for the previous note
        if current_note is not None:
            track.append(Message('note_off', note=current_note, velocity=velocity, time=current_duration))

        # Add a note-on message for the new note
        track.append(Message('note_on', note=note, velocity=velocity, time=0))

        # Update the current note and reset the duration
        current_note = note
        current_duration = 0

    # Increment the duration
    current_duration += 30  # Adjust the time increment as needed

# Add a note-off message for the last note
if current_note is not None:
    track.append(Message('note_off', note=current_note, velocity=velocity, time=current_duration))

# Save the MIDI file
midi_file.save('piano_output.mid')

# Optionally, plot the blue channel values for visualization
blue_values = [color[2] for color in average_colors]
plt.plot(blue_values)
plt.xlabel('Frame')
plt.ylabel('Blue Channel Value')
plt.show()
