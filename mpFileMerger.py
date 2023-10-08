from moviepy.editor import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

def mpFileMerger(video: str):

    # Load the MP4 video
    video_clip = VideoFileClip(video)

    # Load the MP3 audio
    audio_clip = AudioFileClip("Output/output_music.wav")

    # Set the audio of the video to the loaded MP3 audio
    video_clip = video_clip.set_audio(audio_clip)

    # Write the result to a new MP4 file
    video_clip.write_videofile("Output/output_video.mp4", codec="libx264")