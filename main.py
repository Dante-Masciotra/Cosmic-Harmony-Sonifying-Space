import tkinter as tk
from GetRGB import *
from ToSound import *
from mpFileMerger import *
from moviepy.editor import VideoFileClip

# Define the path to the rendered video file
rendered_video_path = "Output/output_video.mp4"

# Create a global variable to store the VideoFileClip object
video_clip = None

def execute():
    # Step 1: Run video file, looking at just a small square in the center, output the average color of every frame in that square
    GetRGB(video='Data/Cosmic Reef [1280 X 720].mp4', x_coord=640, y_coord=360, width_height=75)

    # Step 2: Convert those RGB values into a midi file, then convert the midi file into a WAV
    ToSound(soundfile="Touhou.sf2")

    # Step 3: Combine the WAV and original MP4 for a final video + audio file
    mpFileMerger(video='Data/Cosmic Reef [1280 X 720].mp4')

    # Step 4: Clean up the files made along the way
    show_play_button()

def show_play_button():
    play_button.pack()  # Show the "Play Video" button after rendering is complete

def play_video():
    global video_clip
    video_clip = VideoFileClip(rendered_video_path)

    # Play the video using the default video player (requires a GUI environment)
    video_clip.preview()



app = tk.Tk()
app.title("Sonification of Space Environments.")
app.geometry("400x300")

label = tk.Label(app, text="Play Video")
label.pack()

submit_button = tk.Button(app, text="Submit", command=execute)
submit_button.pack()

play_button = tk.Button(app, text="Play Video", command=play_video)
play_button.pack()
play_button.pack_forget()  # Initially hide the "Play Video" button

app.mainloop()
