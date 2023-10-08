import pygame
import sys
from pygame.locals import *
import cv2
import os
from PIL import Image
from moviepy.editor import VideoFileClip
from GetRGB import *
from ToSound import *
from mpFileMerger import *
import tkinter as tk

video_path = "Data\Cosmic Reef [1280 X 720].mp4"
box_x, box_y = 20, 40
loading_message = None
pygame_running = True

background_color = (0, 0, 0)
button_color = (0, 128, 0)
button_hover_color = (0, 160, 0)
text_box_color = (100, 100, 100)
text_color = (255, 255, 255)

def file_select():
    user_profile = os.environ['USERPROFILE']
    initial_dir = os.path.join(user_profile, 'Videos')
    try:
        subprocess.Popen(['explorer', initial_dir])
    except Exception as e:
        print(f"Error opening File Explorer: {e}")

def execute_program(screen):
    global pygame_running
    print(f"Executing program with coordinates - X: {box_x}, Y: {box_y}, Size: {box_size}")
    GetRGB(video=video_path, x_coord=box_x, y_coord=box_y, width_height=box_size)
    ToSound(soundfile="Touhou.sf2")
    mpFileMerger(video=video_path)
    
    show_play_button()

    pygame_running = False
    pygame.quit()
    


def open_coordinate_selector(rad):
    global box_x, box_y, pygame_running, box_size
    box_size = rad
    pygame.init()

    try:
        video_clip = VideoFileClip(video_path)
        video_width, video_height = video_clip.size
        print(video_width)
        box_x, box_y = (video_width / 2) - 20, (video_height / 2) - 40
        screen_width = video_width + 40
        screen_height = video_height + 90
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Select Coordinates")

        cap = cv2.VideoCapture(video_path)

        ret, frame = cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            thumbnail = Image.fromarray(frame_rgb)
            thumbnail = pygame.image.fromstring(thumbnail.tobytes(), thumbnail.size, thumbnail.mode)
        else:
            thumbnail = pygame.Surface((video_width, video_height))

        thumbnail_rect = thumbnail.get_rect(center=(video_width // 2 + 20, video_height // 2 + 40))
    except Exception as e:
        print(f"Error rendering thumbnail: {str(e)}")
        return

    clock = pygame.time.Clock()
    dragging = False
    snapping = False

    while pygame_running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame_running = False
            elif event.type == MOUSEBUTTONDOWN:
                if thumbnail_rect.collidepoint(event.pos):
                    x, y = event.pos
                    box_x = max(0, min(x - box_size // 2, video_width - box_size + 20))
                    box_y = max(0, min(y - box_size // 2, video_height - box_size + 40))
                    snapping = True

        screen.fill(background_color)
        screen.blit(thumbnail, thumbnail_rect)
        pygame.draw.rect(screen, (255, 0, 0), (box_x, box_y, box_size, box_size), 2)
        exit_button = pygame.Rect(350, screen_height - 40, 50, 30)
        pygame.draw.rect(screen, (255, 0, 0), exit_button)
        pygame.draw.rect(screen, (0, 0, 0), exit_button, 2)
        exit_font = pygame.font.Font(None, 24)
        exit_text = exit_font.render("Exit", True, (255, 255, 255))
        screen.blit(exit_text, (exit_button.x + 5, exit_button.y + 5))
        if event.type == MOUSEBUTTONDOWN and exit_button.collidepoint(event.pos):
            quit_pygame()
        pygame.display.flip()
        clock.tick(30)

def quit_pygame():
    global pygame_running
    pygame_running = False
    pygame.quit() 
    
def show_play_button():
    label2.pack_forget()
    XY_button.pack_forget()
    submit_button.pack_forget()
    label.pack_forget()
    square.pack_forget()
    play_button.pack() 

def play_video():
    global video_clip
    
    video_clip = VideoFileClip("Output/output_video.mp4")
    video_clip.preview()
    sys.exit()

app = tk.Tk()
app.title("Sonification of Space Environments.")
app.geometry("400x300")

label = tk.Label(app, text="Square size in px")
label.pack()
square = tk.Entry(app)
square.insert(0, 175)
square.pack()

XY_button = tk.Button(app, text="Set X and Y Cords", command=lambda: open_coordinate_selector(rad=int(square.get())))
XY_button.pack()

label2 = tk.Label(app, text="Play Video")
label2.pack()

submit_button = tk.Button(app, text="Submit", command=lambda: execute_program(int(square.get())))
submit_button.pack()

play_button = tk.Button(app, text="Play Video", command=play_video)
play_button.pack()
play_button.pack_forget() 

app.mainloop()
