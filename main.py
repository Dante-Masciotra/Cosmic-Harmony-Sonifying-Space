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

# Define global variables
video_path = "Data\Cosmic Reef [1280 X 720].mp4"
box_x, box_y, box_size = 20, 40, 175
loading_message = None

# Define custom colors
background_color = (0, 0, 0)
button_color = (0, 128, 0)
button_hover_color = (0, 160, 0)
text_box_color = (100, 100, 100)
text_color = (255, 255, 255)

def file_select():

    # Use the 'USERPROFILE' environment variable to reference the user's profile folder
    user_profile = os.environ['USERPROFILE']

    # Set the initial directory to a subdirectory in the user's profile folder (you can change this)
    initial_dir = os.path.join(user_profile, 'Videos')

    # Use the 'explorer' command to open the File Explorer
    try:
        subprocess.Popen(['explorer', initial_dir])
    except Exception as e:
        print(f"Error opening File Explorer: {e}")

def execute_program(screen):

    global loading_message
    loading_message = "Executing program..."
    pygame.display.update()

    # Add your code here to execute the program with the selected coordinates
    print(f"Executing program with coordinates - X: {box_x}, Y: {box_y}, Size: {box_size}")
    
    GetRGB(video=video_path, x_coord=box_x, y_coord=box_y, width_height=box_size)

    # Step 2: Convert those RGB values into a midi file, then convert the midi file into a WAV
    ToSound(soundfile="Touhou.sf2")

    # Step 3: Combine the WAV and original MP4 for a final video + audio file
    mpFileMerger(video=video_path)

    pygame.display.quit()
    pygame.quit()
    sys.exit()

def open_coordinate_selector():
    global box_x, box_y, box_size, loading_message
    pygame.init()

    try:
        video_clip = VideoFileClip(video_path)
        video_width, video_height = video_clip.size
        print(video_width)
        box_x, box_y= (video_width/2)-20, (video_height/2)-40
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

    # Custom input box parameters
    input_box = pygame.Rect(20, screen_height - 50, 200, 60)

    font = pygame.font.Font(None, 32)  # Use the default font
    text = ''
    type_line_visible = True
    type_line_timer = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if thumbnail_rect.collidepoint(event.pos):
                    x, y = event.pos
                    box_x = max(20, min(x - box_size // 2, video_width - box_size + 20))
                    box_y = max(40, min(y - box_size // 2, video_height - box_size + 40))
                    snapping = True
                elif input_box.collidepoint(event.pos):
                    text = ''
            elif event.type == MOUSEBUTTONUP:
                snapping = False
            elif event.type == MOUSEMOTION and dragging:
                if not snapping:
                    x, y = event.pos
                    box_x = max(20, min(x - box_size // 2, video_width - box_size + 20))
                    box_y = max(40, min(y - box_size // 2, video_height - box_size + 40))
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    try:
                        box_size = int(text)
                    except ValueError:
                        pass
                    text = ''
                elif event.key == K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        screen.fill(background_color)

        # Draw the loading message if it's present
        if loading_message is not None:
            loading_font = pygame.font.Font(None, 36)  # Use the default font
            loading_text = loading_font.render(loading_message, True, (255, 255, 255))
            loading_text_rect = loading_text.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(loading_text, loading_text_rect)

        screen.blit(thumbnail, thumbnail_rect)

        # Draw the draggable rectangle
        pygame.draw.rect(screen, (255, 0, 0), (box_x, box_y, box_size, box_size), 2)

        # Draw the custom input box
        pygame.draw.rect(screen, text_box_color, input_box, 0)  # Filled rectangle for text box
        pygame.draw.rect(screen, (255, 255, 255), input_box, 2)  # Border for text box
        input_text = font.render(text, True, text_color)

        screen.blit(input_text, (input_box.x + 5, input_box.y + 5))

        # Flashing type line when active
        

        if type_line_visible:
            pygame.draw.line(screen, (0, 0, 0), (input_box.x + 5 + input_text.get_width(), input_box.y + 5),
                             (input_box.x + 5 + input_text.get_width(), input_box.y + 5 + input_box.height), 2)

        # Add a styled "Execute" button
        execute_button = pygame.Rect(250, screen_height - 40, 100, 30)
        pygame.draw.rect(screen, button_color, execute_button, 0)
        pygame.draw.rect(screen, (0, 0, 0), execute_button, 2)  # Border for the button
        execute_font = pygame.font.Font(None, 24)
        execute_text = execute_font.render("Execute", True, (255, 255, 255))
        screen.blit(execute_text, (execute_button.x + 15, execute_button.y + 5))

        # Add a styled "File Select" button
        file_button = pygame.Rect(450, screen_height - 40, 125, 30)
        pygame.draw.rect(screen, button_color, file_button, 0)
        pygame.draw.rect(screen, (0, 0, 0), file_button, 2)  # Border for the button
        file_font = pygame.font.Font(None, 24)
        file_text = file_font.render("Select a File", True, (255, 255, 255))
        screen.blit(file_text, (file_button.x + 15, file_button.y + 5))

        # Check if the "Execute" button is clicked
        if event.type == MOUSEBUTTONDOWN and file_button.collidepoint(event.pos):
            file_select()

        # Check if the "Execute" button is clicked
        if event.type == MOUSEBUTTONDOWN and execute_button.collidepoint(event.pos):
            execute_program(screen)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    open_coordinate_selector()
