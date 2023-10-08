from moviepy.editor import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

def mpFileMerger(video: str):

    # 2 input files
    video_clip = VideoFileClip(video)
    audio_clip = AudioFileClip("Output/output_music.wav")

    # Combine Audio with Video
    video_clip = video_clip.set_audio(audio_clip)

    # Output new combined MP4
    video_clip.write_videofile("Output/output_video.mp4", codec="libx264")