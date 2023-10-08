import cv2
import numpy as np

def GetRGB(video: str, x_coord: int, y_coord: int, width_height: int):

    # Replace 'your_video.mp4' with the path to your video file
    video_path = video
    cap = cv2.VideoCapture(video_path)
    average_colors = []
    flag=True
    while True:
        # Read the next frame from the video
        ret, frame = cap.read()

        # Break the loop if we've reached the end of the video
        if not ret:
            break

        # Crop a 50x50 section from the frame (you can adjust the coordinates as needed)
        x, y, width, height = x_coord, y_coord, width_height, width_height
        cropped_section = frame[y:y+height, x:x+width]

        # Get the average color of the cropped section
        avg_color = np.mean(cropped_section, axis=(0, 1)).astype(int)

        # Append the average color (in RGB format) to the list
        average_colors.append(avg_color)

        # Display the original frame and the cropped section
        # cv2.imshow('Original Frame', frame)
        # cv2.imshow('Cropped Section', cropped_section)
        if flag:
            print('Loading')
            flag=False

        # Break the loop if the user presses the 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Release the video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()
    print('Complete')

    # Write the list of average colors in RGB format to a text file
    output ='Output/average_colors.txt'
    with open(output, 'w') as file:
        for color in average_colors:
            file.write(f'RGB: {color[2]}, {color[1]}, {color[0]}\n')


if __name__ == '__main__':

    GetRGB(video= 'Data/Cosmic Reef [1280 X 720].mp4', x_coord= 640, y_coord= 360, width_height= 75)
