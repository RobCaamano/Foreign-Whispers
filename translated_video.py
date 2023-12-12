from moviepy.editor import VideoFileClip, AudioFileClip
from pydub import AudioSegment
import srt
import datetime
import ffmpeg
import os
import re
import random

def create_translated_video(original_video_path, translated_audio_path, translated_text_path, video_name, output_dir='./translated'):
    # Load original video
    video = VideoFileClip(original_video_path)

    # Load TTS audio
    new_audio = AudioFileClip(translated_audio_path)
    video = video.set_audio(new_audio)
    audio_segment = AudioSegment.from_file(translated_audio_path, format="wav")

    # Check if new audio is shorter to pad with silence
    if new_audio.duration < video.duration:
        silence_duration = (video.duration - new_audio.duration) * 1000  # convert to milliseconds
        silence_segment = AudioSegment.silent(duration=silence_duration)
        audio_segment = audio_segment + silence_segment
        padded_audio_path = os.path.join(output_dir, 'padded_audio.wav')
        audio_segment.export(padded_audio_path, format='wav')
        new_audio = AudioFileClip(padded_audio_path)

    # Generate SRT content
    def parse_translated_text(file_path):
        with open(file_path, 'r') as file:
            content = file.readlines()

        subtitles = []
        timestamp_pattern = re.compile(r'\[(\d+\.\d+)\-(\d+\.\d+)\]')
        for line in content:
            match = timestamp_pattern.match(line)
            if match:
                start_time = datetime.timedelta(seconds=float(match.group(1)))
                end_time = datetime.timedelta(seconds=float(match.group(2)))
                text = line[match.end():].strip()

                subtitle = srt.Subtitle(index=len(subtitles)+1,
                                        start=start_time,
                                        end=end_time,
                                        content=text)
                subtitles.append(subtitle)

        return srt.compose(subtitles)

    # Generate SRT content
    srt_content = parse_translated_text(translated_text_path)

    # Write to an SRT file
    srt_file = './translated/translated.srt'
    with open(srt_file, 'w', encoding='utf-8') as file:
        file.write(srt_content)

    # Write final video temp file
    temp = "./translated/temp.mp4"
    video.write_videofile(temp)

    # Add subtitles
    ran = random.randint(1000,9999)
    final_video_file = os.path.join(output_dir, f"{video_name}{ran}.mp4")

    # Correct subtitle filter string for ffmpeg
    subtitle_filter_str = f"subtitles='{srt_file}'"

    try:
        ffmpeg.input(temp).output(final_video_file, vf=subtitle_filter_str).run()
    except ffmpeg.Error as e:
        print(f"Error creating final video: {e}")
        return None

    # Remove temp file
    os.remove(temp)
    return final_video_file