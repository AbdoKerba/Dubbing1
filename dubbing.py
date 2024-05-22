# -*- coding: utf-8 -*-
"""Dubbing.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1sVzQCRlH5X9Wut8Pm6b-7d3VKflOgYGD
"""

# !pip install pytube
# !pip install git+https://github.com/openai/whisper.git
# !pip install ffmpeg
# !pip install deep_translator
# !pip install subtoaudio
# !pip install TTS

# !pip install -r requirements.txt

cd Dubbing1/

from pytube import YouTube
import os

def download_video_with_resolution_and_name(youtube_url, save_path, resolution, file_name):
    try:
        # Create a YouTube object with the provided URL
        yt = YouTube(youtube_url)

        # Filter streams by resolution
        filtered_streams = yt.streams.filter(res=f'{resolution}p', progressive=True, file_extension='mp4', mime_type='video/mp4')

        if not filtered_streams:
            print(f"No streams available for resolution {resolution}p.")
            return

        # Get the first stream (you can adjust this based on your preference)
        stream = filtered_streams[0]

        # Download the video with custom name
        file_path = os.path.join(save_path, f"{file_name}.mp4")
        stream.download(output_path=save_path, filename=file_name)

        print("Video downloaded successfully!")
    except Exception as e:
        print("Error:", str(e))

# Example usage
if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=cJTXh7g-uCM&ab_channel=AmitThinks"
    save_directory = os.getcwd()
    desired_resolution = 360  # Specify the desired resolution here
    custom_file_name = os.getcwd() + "/video.mp4"  # Specify the custom file name here
    download_video_with_resolution_and_name(video_url, save_directory, desired_resolution, custom_file_name)

from moviepy.editor import VideoFileClip , AudioFileClip
import os
# Define the input video file and output audio file
mp4_file = os.getcwd() + "/video.mp4"
audio_file = os.getcwd() + "/audio.mp3"

# Load the video clip
video_clip = VideoFileClip(mp4_file)

# Extract the audio from the video clip
audio_clip = video_clip.audio

# Write the audio to a separate file
audio_clip.write_audiofile(audio_file)

# Close the video and audio clips
audio_clip.close()
video_clip.close()





import whisper
from datetime import timedelta

model = whisper.load_model("medium")

result = model.transcribe(audio_file)

from whisper.utils import get_writer
txt_writer = get_writer("srt", os.getcwd())
txt_writer(result, audio_file)



from deep_translator import GoogleTranslator
import datetime

srt_aud_file = audio_file.split('.')[0]
translated_subs = ''
with open(f"{srt_aud_file}.srt", "r", encoding="utf-8") as txt:
  for line in txt.readlines():
    translated_subs += f"{GoogleTranslator(source='en', target='ar').translate(line)}\n"
with open(f"{srt_aud_file}_ar.srt",mode='w') as sub_output:
    sub_output.write(translated_subs)

"""Text To Speech"""



from subtoaudio import SubToAudio

# Initialize SubToAudio with a Coqui TTS model (e.g., English)
sub = SubToAudio(model_name="tts_models/multilingual/multi-dataset/xtts_v2", )

#load pretrained model
# sub = SubToAudio(config_path="/content/drive/MyDrive/tts_models/config.json" , model_path='/content/drive/MyDrive/tts_models/')

sub_file_name = f'{srt_aud_file}_ar.srt'
tempo_limit = 3

# Provide the path to your subtitle file (e.g., 'yoursubtitle.srt')
subtitle = sub.subtitle(f"/{sub_file_name}")

# Convert subtitle data to audio
sub.convert_to_audio(sub_data=subtitle, output_path= f"{srt_aud_file}_ar",tempo_mode='overflow', speaker_wav=f"{audio_file}" , language='ar', tempo_limit=tempo_limit)

# Load the video and audio clips
video_clip = VideoFileClip(mp4_file)
new_audio_clip = AudioFileClip(f"{os.getcwd()}/audio_ar.wav")

# Remove the original audio from the video
video_without_audio = video_clip.without_audio()

# Set the new audio to the video
final_video = video_without_audio.set_audio(new_audio_clip)

# Save the final video
final_video.write_videofile(f"{os.getcwd()}/output_video.mp4", codec="libx264", audio_codec="aac")

# import locale
# locale.getpreferredencoding = lambda: "UTF-8"

# !cp /content/output_video.mp4 /content/drive/MyDrive/output_video.mp4
