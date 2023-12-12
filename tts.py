from TTS.api import TTS
from pydub import AudioSegment
import os
import re
import ffmpeg
import shutil
import argparse
import torch

'''
    PLEASE NOTE:
    tts_speed initially 1.0 and increases to 2.0 if necessary. This has been commented out for improved execution times due to CPU usage. 
    Feel free to remove comments when used locally.
'''

# Accept TOS for tts
os.environ["COQUI_TOS_AGREED"] = "1"

# Adjust speed of audio segment
def adjust_speed(input_file, speed_factor):
    output_file = input_file.replace(".wav", "_adjusted.wav")
    ffmpeg.input(input_file).filter('atempo', speed_factor).output(output_file, acodec='pcm_s16le').run()
    return output_file

# Generate and process speech for each line
def generate_speech(text, speaker_voice_map, output_file):
    combined_audio = AudioSegment.empty()
    temp_files = []

    if torch.cuda.is_available():
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cuda")
    else:
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

    for line in text.split("\n"):
        if not line.strip():
            continue

        # Extract speaker ID, timestamps & text
        match = re.match(r"\[SPEAKER_(\d+)\] \[(\d+\.\d+)-(\d+\.\d+)\] (.+)", line)
        if not match:
            continue

        speaker_id, start_time, end_time, sentence = match.groups()
        start_time, end_time = float(start_time), float(end_time)
        segment_duration = (end_time - start_time) * 1000  # Duration in milliseconds

        speaker_wav = speaker_voice_map.get(f"SPEAKER_{speaker_id}")
        if not speaker_wav:
            continue

        # Create temp
        os.makedirs('./audio/temp', exist_ok=True)
        temp_file_path = f"./audio/temp/temp_output_part_{len(temp_files)}.wav"
        temp_files.append(temp_file_path)

        # Initial TTS (original : 1.0 speed)
        tts_speed = 2.0 # original 1.0
        tts.tts_to_file(text=sentence, file_path=temp_file_path, speaker_wav=speaker_wav, language="es", speed=tts_speed)

        segment_audio = AudioSegment.from_wav(temp_file_path)

        # Increase TTS speed if audio is longer than duration
        if segment_audio.duration_seconds * 1000 > segment_duration:
            #while tts_speed < 2.0 and segment_audio.duration_seconds * 1000 > segment_duration:
            #    tts_speed += 0.5
            #    tts.tts_to_file(text=sentence, file_path=temp_file_path, speaker_wav=speaker_wav, language="es", speed=tts_speed)
            #    segment_audio = AudioSegment.from_wav(temp_file_path)

            # Speed up using FFmpeg if audio is longer than duration
            if segment_audio.duration_seconds * 1000 > segment_duration:
                required_speed = segment_duration / (segment_audio.duration_seconds * 1000)
                if required_speed < 1.0:
                    required_speed = 1.0 / required_speed
                temp_file_path = adjust_speed(temp_file_path, required_speed)
                segment_audio = AudioSegment.from_wav(temp_file_path)

        # Add silence at start of audio if needed
        if combined_audio.duration_seconds == 0 and start_time > 0:
            combined_audio = AudioSegment.silent(duration=start_time * 1000) + combined_audio

        # Trim or pad audio to match segment duration (Should not trim since audio sped up)
        if segment_audio.duration_seconds * 1000 > segment_duration:
            segment_audio = segment_audio[:segment_duration]
        else:
            segment_audio = segment_audio + AudioSegment.silent(duration=segment_duration - len(segment_audio))

        combined_audio += segment_audio

    # Export combined audio
    combined_audio.export(output_file, format="wav")

    # Delete temp files
    for temp_file in temp_files:
        os.remove(temp_file)

# Map speaker IDs to their voice files
def map_speaker_ids(directory):
    speaker_voice_map = {}
    for file in os.listdir(directory):
        if file.endswith(".wav"):
            speaker_id = file.replace(".wav", "")
            speaker_voice_map[speaker_id] = os.path.join(directory, file)
    return speaker_voice_map

def main(speaker_directory, aligned_text_file, output_audio_file):
    # Generate speaker voice map and read translated text
    speaker_voice_map = map_speaker_ids(speaker_directory)
    with open(aligned_text_file, 'r') as file:
        translated_text = file.read()

    # Generate speech
    generate_speech(translated_text, speaker_voice_map, output_audio_file)

    # Remove temp folder
    if os.path.exists('./audio/temp'):
        shutil.rmtree('./audio/temp')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate speech from translated text")
    parser.add_argument("speaker_directory", help="Directory containing speaker voice clips")
    parser.add_argument("aligned_text_file", help="Path to the translated and aligned text file")
    parser.add_argument("output_audio_file", help="Path to save the generated speech audio file")
    args = parser.parse_args()

    main(args.speaker_directory, args.aligned_text_file, args.output_audio_file)
