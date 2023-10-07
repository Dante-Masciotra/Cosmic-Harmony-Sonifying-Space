import os
from pydub import AudioSegment
def midi_to_mp3(midi_file, soundfont, mp3_file):
    # Convert MIDI to WAV using fluidsynth
    wav_file = mp3_file.replace('.mp3', '.wav')
    os.system(f'fluidsynth -ni {soundfont} {midi_file} -F {wav_file} -r 44100')
    # Convert WAV to MP3 using pydub
    audio = AudioSegment.from_wav(wav_file)
    audio.export(mp3_file, format='mp3')
    # Remove temporary WAV file
    os.remove(wav_file)
# Example usage:
midi_file = 'input.mid'
soundfont = 'path/to/GeneralUser GS.sf2'
mp3_file = 'output.mp3'
midi_to_mp3(midi_file, soundfont, mp3_file)

#Replace 'input.mid', 'path/to/GeneralUser GS.sf2', and 'output.mp3' with the appropriate file paths. 
# This script will convert the specified MIDI file to MP3 using the specified SoundFont.

#SoundFont files contain samples of musical instruments, and are required by fluidsynth 
# to generate audio from MIDI. A popular free SoundFont is GeneralUser GS, which can be downloaded from the schristiancollins website.