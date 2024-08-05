from pyannote.audio import Pipeline
from pydub import AudioSegment
import os
import re
import torch

def perform_diarization(audio_file_path, translated_file_path, output_dir='./audio/diarization'):

    # Initialize diarization pipeline
    #accesstoken = os.environ['Diarization']
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1")

    # Send pipeline to GPU (when available)
    pipeline.to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))

    # Load audio file
    audio = AudioSegment.from_wav(audio_file_path)

    # Apply pretrained pipeline
    diarization = pipeline(audio_file_path)

    os.makedirs(output_dir, exist_ok=True)

    # Process and save each speaker's audio segments
    speaker_segments_audio = {}
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        start_ms = int(turn.start * 1000)  # Convert to milliseconds
        end_ms = int(turn.end * 1000)      # Convert to milliseconds
        segment = audio[start_ms:end_ms]

        if speaker in speaker_segments_audio:
            speaker_segments_audio[speaker] += segment
        else:
            speaker_segments_audio[speaker] = segment

    # Save audio segments
    for speaker, segment in speaker_segments_audio.items():
        output_path = os.path.join(output_dir, f"{speaker}.wav")
        segment.export(output_path, format="wav")
        print(f"Combined audio for speaker {speaker} saved in {output_path}")

    # Load translated text
    with open(translated_file_path, "r") as file:
        translated_lines = file.readlines()

    # Process and align translated text with diarization data
    last_speaker = None
    aligned_text = []
    timestamp_pattern = re.compile(r'\[(\d+\.\d+)\-(\d+\.\d+)\]')
    for line in translated_lines:
        match = timestamp_pattern.match(line)
        
        if match:
            start_time = float(match.group(1))
            end_time = float(match.group(2))
            text = line[match.end():].strip()  # Extract text part

            speaker_found = False
            # Find corresponding speaker
            for turn, _, speaker in diarization.itertracks(yield_label=True):
                speaker_start = turn.start
                speaker_end = turn.end
                # Check for overlap between speaker segment and line timestamp
                if max(speaker_start, start_time) < min(speaker_end, end_time):
                    aligned_text.append(f"[{speaker}] [{start_time}-{end_time}] {text}")
                    speaker_found = True
                    last_speaker = speaker
                    break

            # If no speaker found, use the last speaker
            if not speaker_found:
                if last_speaker is not None:
                    aligned_text.append(f"[{last_speaker}] [{start_time}-{end_time}] {text}")
                else:
                    aligned_text.append(f"[Unknown Speaker] [{start_time}-{end_time}] {text}")

    # Save aligned text to a single file
    aligned_text_output_path = os.path.join(output_dir, "aligned_text.txt")
    with open(aligned_text_output_path, "w") as aligned_text_file:
        aligned_text_file.write('\n'.join(aligned_text))
    print(f"Aligned text saved in {aligned_text_output_path}")
