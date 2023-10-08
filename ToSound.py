import numpy as np
from mido import MidiFile, MidiTrack, Message
import subprocess

def ToSound(soundfile: str):
    # Read the list of average colors from the text file
    average_colors = []
    with open('Output/average_colors.txt', 'r') as file:
        for line in file:
            # Split the line into individual RGB values and convert them to integers
            r, g, b = map(int, line.strip('RGB: \n').split(', '))
            color = np.array([r, g, b])
            average_colors.append(color)

    # Create a MIDI file
    midi_file = MidiFile()
    # Create separate tracks for each color channel
    track_blue = MidiTrack()
    track_red = MidiTrack()
    track_green = MidiTrack()
    midi_file.tracks.extend([track_blue, track_red, track_green])

    # Define MIDI note numbers corresponding to the desired pitch range
    min_note = 20  # MIDI note number for C4
    max_note = 107  # MIDI note number for C7

    # Define program numbers (patch numbers) for each instrument
    program_blue = 16  # Acoustic Grand Piano
    program_red = 42  # Saxophone
    program_green = 69  # Standard MIDI drum kit (High Q)

    # Initialize variables to track the current note and its duration for each channel
    current_notes = [None, None, None]
    current_durations = [0, 0, 0]

    # Normalize the color channels to the range [0, 1] and map them to MIDI notes
    for color in average_colors:
        blue_normalized = color[2] / 255.0  # Normalize blue channel
        red_normalized = color[0] / 255.0  # Normalize red channel
        green_normalized = color[1] / 255.0  # Normalize green channel

        notes = [int(min_note + (max_note - min_note) * blue_normalized),
                int(min_note + (max_note - min_note) * red_normalized),
                int(min_note + (max_note - min_note) * green_normalized)]

        velocity = 64  # Set the velocity (volume) of the note

        # Assign program change and notes for each channel
        for i in range(len(current_notes)):
            if notes[i] != current_notes[i]:
                if current_notes[i] is not None:
                    track = [track_blue, track_red, track_green][i]
                    track.append(Message('note_off', note=current_notes[i], velocity=velocity, time=current_durations[i]))
                track = [track_blue, track_red, track_green][i]
                track.append(Message('program_change', program=[program_blue, program_red, program_green][i]))
                track.append(Message('note_on', note=notes[i], velocity=velocity, time=0))
                current_notes[i] = notes[i]
                current_durations[i] = 0

            current_durations[i] += 30  # Adjust the time increment as needed

    # Add note-off messages for the last notes
    for i in range(len(current_notes)):
        if current_notes[i] is not None:
            track = [track_blue, track_red, track_green][i]
            track.append(Message('note_off', note=current_notes[i], velocity=velocity, time=current_durations[i]))

    # Save the MIDI file
    midi_file.save('Output/output_music.mid')

    # Specify the input MIDI file and output WAV file
    input_midi_file = "Output/output_music.mid"
    output_wav_file = "Output/output_music.wav"
    soundfont_file = soundfile  # Replace with the path to your SoundFont file

    # Convert the MIDI file to WAV using FluidSynth
    try:
        subprocess.run(["fluidsynth", "-T", "wav", soundfont_file, input_midi_file, "-F", output_wav_file], check=True)
        print(f"Conversion completed: {input_midi_file} -> {output_wav_file}")
    except subprocess.CalledProcessError:
        print("Error: MIDI to WAV conversion failed.")