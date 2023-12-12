from transformers import MarianMTModel, MarianTokenizer
from tqdm import tqdm
import os
import re
import argparse

# Load Model and Tokenizer
model_name = "Helsinki-NLP/opus-mt-en-es"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

# Extract & separate timestamp and text
def extract_timestamp_and_text(line):
    match = re.match(r'\[(\d+\.\d+\-\d+\.\d+)\]\s+(.*)', line)
    if match:
        return match.group(1), match.group(2)
    return '', line

# Translate text
def translate_text(text):
    lines = text.split('\n')
    translated_lines = []

    for line in tqdm(lines, desc="Translating lines", leave=False):
        # Check if line empty
        if not line.strip():
            translated_lines.append('')
            continue

        timestamp, line_text = extract_timestamp_and_text(line)

        # Translate text
        if line_text.strip():
            model_inputs = tokenizer(line_text, return_tensors="pt", truncation=True, padding="longest")
            translated = model.generate(**model_inputs)
            translated_text = tokenizer.batch_decode(translated, skip_special_tokens=True)[0]
            translated_line = f'[{timestamp}] {translated_text}'
        else:
            translated_line = f'[{timestamp}]'

        translated_lines.append(translated_line)

    return '\n'.join(translated_lines)

# Main function to translate a file
def translate_file(src_file_path, dst_file_path):
    try:
        with open(src_file_path, 'r') as file:
            english_text = file.read()
            spanish_text = translate_text(english_text)
        
        with open(dst_file_path, 'w') as file:
            file.write(spanish_text)
        print(f"Translation completed: {dst_file_path}")

    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Translate English text to Spanish")
    parser.add_argument("src_file_path", help="Path to the source file with English text")
    parser.add_argument("dst_file_path", help="Path to save the translated Spanish text")
    args = parser.parse_args()

    translate_file(args.src_file_path, args.dst_file_path)
