# Master file to run the full termial version of Sonification

from GetRGB import *
from ToSound import *
from mpFileMerger import *
import tkinter as tk



def execute():
    # Step 1: Run video file, looking at just a small square in the centre, output the average colour of every frame in that square
    GetRGB(video= 'Data/Cosmic Reef [1280 X 720].mp4', x_coord= 640, y_coord= 360, width_height= 75)
    

    # Step 2: Convert those RGB values into a midi file, then convert the midi file into a WAV
    ToSound(soundfile= "Text/Touhou.sf2")

    # Step 3: Combine the WAV and original MP4 for a final video + audio file
    mpFileMerger(video= 'Data/Cosmic Reef [1280 X 720].mp4')

    # Step 4: Clean up the files made along the way

def on_submit():
    execute()

app = tk.Tk()
app.title("Sonnification in of Space Environments.")
app.geometry("400x300")

label = tk.Label(app, text="Play Video")
label.pack()

submit_button = tk.Button(app, text="Submit", command=on_submit)
submit_button.pack()

app.mainloop()
