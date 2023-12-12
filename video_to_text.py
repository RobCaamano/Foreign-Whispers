import argparse
from moviepy.editor import VideoFileClip
import whisper
import os
import re

# Extracts audio from video
def extract_audio(video_path, audio_dir='./audio'):
    os.makedirs(audio_dir, exist_ok=True)
    base_filename = os.path.splitext(os.path.basename(video_path))[0]
    audio_filename = os.path.join(audio_dir, base_filename + '.wav')
    video_clip = VideoFileClip(video_path)
    video_clip.audio.write_audiofile(audio_filename)
    video_clip.close()
    return audio_filename

# Transcribe audio .wav file
def transcribe_audio(audio_path, model_type='base', transcribed_dir='./transcribed'):
    model = whisper.load_model(model_type)
    result = model.transcribe(audio_path)
    
    os.makedirs(transcribed_dir, exist_ok=True)
    base_filename = os.path.splitext(os.path.basename(audio_path))[0]
    transcribed_filename = os.path.join(transcribed_dir, base_filename + '.txt')

    with open(transcribed_filename, 'w') as file:
        for segment in result['segments']:
            start = segment['start']
            end = segment['end']
            text = segment['text']
            file.write(f"[{start:.2f}-{end:.2f}] {text}\n")
    
    return transcribed_filename, result['text']

# Merge lines in file that are part of the same sentence
def merge_lines(file_path):
    timestamp_pattern = re.compile(r'\[(\d+\.\d+)-(\d+\.\d+)\]')

    with open(file_path, 'r') as file:
        lines = file.readlines()

    merged_lines = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()
        match = timestamp_pattern.match(line)

        if match:
            start_time = float(match.group(1))
            text = line[match.end():].strip()

            # Check if line doesnt end
            if not (text.endswith('.') or text.endswith('?')):
                # Merge with the next line
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    next_match = timestamp_pattern.match(next_line)
                    
                    if next_match:
                        end_time = float(next_match.group(2))
                        next_text = next_line[next_match.end():].strip()
                        merged_text = text + ' ' + next_text
                        merged_line = f"[{start_time:.2f}-{end_time:.2f}] {merged_text}\n"
                        merged_lines.append(merged_line)
                        i += 1
            else:
                end_time = float(match.group(2))
                merged_lines.append(f"[{start_time:.2f}-{end_time:.2f}] {text}\n")

        i += 1

    # Overwrite original file with merged lines
    with open(file_path, 'w') as file:
        file.writelines(merged_lines)

    return file_path

# Driver function
def convert_video_to_text(video_file_path, model_type='base'):
    # Extract audio
    audio_path = extract_audio(video_file_path)

    # Transcribe audio
    transcribed_path, _ = transcribe_audio(audio_path, model_type)

    # Merge lines
    merge_lines(transcribed_path)
    
    return transcribed_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe audio from video")
    parser.add_argument("video_file", help="Path to the video file")
    parser.add_argument("--model", help="Size of the whisper model (e.g., tiny, base, small, medium, large, huge).", default="base")
    args = parser.parse_args()

    convert_video_to_text(args.video_file, args.model)
