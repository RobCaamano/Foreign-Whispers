import argparse
import os
from yt_download import download_video
from video_to_text import convert_video_to_text
from opus import translate_file
from diarization import perform_diarization
from tts import main as tts_main
from translated_video import create_translated_video

def get_transcription_filename(video_path):
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    return f'./transcribed/{base_name}.txt'

def get_audio_filename(video_path):
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    return f'./audio/{base_name}.wav'

def get_video_name(video_path):
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    return base_name

def main(youtube_url):
    # Ensure necessary directories exist
    if not os.path.exists('./downloads'):
        os.makedirs('./downloads')
    if not os.path.exists('./audio'):
        os.makedirs('./audio')
    if not os.path.exists('./transcribed'):
        os.makedirs('./transcribed')
    if not os.path.exists('./translated'):
        os.makedirs('./translated')

    # Step 1: Download video
    ## yt_download.py
    downloaded_video_path = download_video(youtube_url)

    # Step 2: Transcribe video's audio
    ## video_to_text.py
    transcribed_text_path = get_transcription_filename(downloaded_video_path)
    model_type = 'base' # Whisper model type
    convert_video_to_text(downloaded_video_path, model_type)


    # Step 3: Translate transcribed text to Spanish
    ## opus.py
    translated_text_path = './translated/translated_text.txt'
    translate_file(transcribed_text_path, translated_text_path)

    # Step 4: Perform diarization
    ## diarization.py
    audio_path = get_audio_filename(downloaded_video_path)
    diarized_audio_dir = './audio/diarization'
    perform_diarization(audio_path, translated_text_path)

    # Step 5: Generate speech for translated text
    ## tts.py
    speaker_directory = './audio/diarization'
    aligned_text_file = './audio/diarization/aligned_text.txt'
    output_audio_file = './translated/final_audio.wav'
    tts_main(speaker_directory, aligned_text_file, output_audio_file)

    # Step 6: Create final translated video
    ## translated_video.py
    video_name = get_video_name(downloaded_video_path)
    final_video_path = create_translated_video(downloaded_video_path, output_audio_file, translated_text_path, video_name)

    print(f"Final translated video created at {final_video_path}")

    return final_video_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a YouTube video with multiple steps.")
    parser.add_argument("youtube_url", help="YouTube video URL")
    args = parser.parse_args()

    main(args.youtube_url)