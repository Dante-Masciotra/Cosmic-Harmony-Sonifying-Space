import pygame
import sys
from pygame.locals import *
import cv2  # Import OpenCV
from PIL import Image
from moviepy.editor import VideoFileClip
from GetRGB import *
from ToSound import *
from mpFileMerger import *

# Define global variables
rendered_video_path = "Output/output_video.mp4"
box_x, box_y, box_size = 20, 40, 175
loading_message = None

def execute_program(screen):
    global loading_message
    loading_message = "Executing program..."
    pygame.display.update()  # Update the display to show the loading message

    # Add your code here to execute the program with the selected coordinates
    print(f"Executing program with coordinates - X: {box_x}, Y: {box_y}, Size: {box_size}")
    # Step 1: Run video file, looking at just a small square in the centre, output the average colour of every frame in that square
    GetRGB(video='Data/Cosmic Reef [1280 X 720].mp4', x_coord=box_x, y_coord=box_y, width_height=box_size)

    # Step 2: Convert those RGB values into a midi file, then convert the midi file into a WAV
    ToSound(soundfile="Touhou.sf2")

    # Step 3: Combine the WAV and original MP4 for a final video + audio file
    mpFileMerger(video='Data/Cosmic Reef [1280 X 720].mp4')

    loading_message = "Execution complete!"
    pygame.display.update()  # Update the display to show the completion message
    pygame.time.delay(2000)  # Add a delay to keep the completion message visible for 2 seconds
    loading_message = None  # Clear the loading message

def open_coordinate_selector():
    global box_x, box_y, box_size, loading_message
    pygame.init()

    try:
        video_clip = VideoFileClip(rendered_video_path)
        video_width, video_height = video_clip.size
        screen_width = video_width + 40  # Add padding to the sides
        screen_height = video_height + 90  # Add padding to the bottom
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Select Coordinates")

        cap = cv2.VideoCapture(rendered_video_path)  # Open the video using OpenCV

        # Capture the first frame to create a thumbnail
        ret, frame = cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
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
    input_box = pygame.Rect(20, screen_height - 50, 200, 60)  # Adjust the width to 180

    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    font = pygame.font.Font(None, 32)
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
                    # Ensure that the red box stays within the thumbnail bounds
                    box_x = max(20, min(x - box_size // 2, video_width - box_size + 20))
                    box_y = max(40, min(y - box_size // 2, video_height - box_size + 40))
                    snapping = True
                elif input_box.collidepoint(event.pos):
                    color = color_active
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
                        pass  # Handle invalid input gracefully
                    text = ''
                elif event.key == K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        screen.fill((0, 0, 0))  # Fill the screen with black

        # Draw the loading message if it's present
        if loading_message is not None:
            loading_font = pygame.font.Font(None, 36)
            loading_text = loading_font.render(loading_message, True, (255, 255, 255))
            loading_text_rect = loading_text.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(loading_text, loading_text_rect)

        screen.blit(thumbnail, thumbnail_rect)

        # Draw the draggable rectangle
        pygame.draw.rect(screen, (255, 0, 0), (box_x, box_y, box_size, box_size), 2)

        # Draw the custom input box
        pygame.draw.rect(screen, color, input_box, 2)
        input_text = font.render(text, True, (255, 255, 255))

        screen.blit(input_text, (input_box.x + 5, input_box.y + 5))

        # Flashing type line when active
        if color == color_active:
            type_line_timer += 1
            if type_line_timer >= 30:
                type_line_timer = 0
                type_line_visible = not type_line_visible

        if type_line_visible and color == color_active:
            pygame.draw.line(screen, (0, 0, 0), (input_box.x + 5 + input_text.get_width(), input_box.y + 5),
                             (input_box.x + 5 + input_text.get_width(), input_box.y + 5 + input_box.height), 2)

        # Add an "Execute" button
        execute_button = pygame.Rect(250, screen_height - 40, 100, 30)
        pygame.draw.rect(screen, (0, 255, 0), execute_button, 0)
        execute_font = pygame.font.Font(None, 24)
        execute_text = execute_font.render("Execute", True, (0, 0, 0))
        screen.blit(execute_text, (execute_button.x + 5, execute_button.y + 5))

        # Check if the "Execute" button is clicked
        if event.type == MOUSEBUTTONDOWN and execute_button.collidepoint(event.pos):
            execute_program(screen)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    open_coordinate_selector()
