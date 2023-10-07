import fluidsynth

# Path to your SoundFont file (SF2)
soundfont_file = "path_to_your_soundfont.sf2"

# Create a FluidSynth instance
fs = fluidsynth.Synth()

# Load the SoundFont
fs.load_soundfont(soundfont_file)

# Path to your MIDI file
midi_file = "input.mid"

# Create an audio driver (e.g., ALSA on Linux, CoreAudio on macOS, or PortAudio on Windows)
# Note: The actual audio driver to use may vary depending on your system. Adjust accordingly.
audio_driver = fluidsynth.AudioDriver()

# Open the audio driver
audio_driver.start()

# Load and play the MIDI file
fs.midi_file_to_audio(midi_file)

# Wait for the MIDI file to finish playing
while fs.get_busy():
    pass

# Close the audio driver
audio_driver.close()

# Clean up and delete the FluidSynth instance
fs.delete()
