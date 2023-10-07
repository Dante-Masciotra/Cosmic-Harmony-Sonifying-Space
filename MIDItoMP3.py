import fluidsynth
fs = fluidsynth.Synth()
# You can find soundfonts online for free, like the one from MuseScore.
# Here's the link: https://musescore.org/en/handbook/3/soundfonts-and-sfz-files#gm
fs.start(driver="alsa") 
sfid = fs.sfload("/path/to/your/soundfont.sf2")
fs.program_select(0, sfid, 0, 0)
# Your MIDI file goes here.
fs.midi_to_audio('/path/to/your/file.mid', '/path/to/output.wav')
fs.delete()