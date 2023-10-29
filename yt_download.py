from pytube import YouTube
from tqdm import tqdm
import os

progress_bar = None

if not os.path.exists('./downloads'):
    os.makedirs('./downloads')

# Updates progress bar
def progress_function(stream, chunk, bytes_remaining):
    global progress_bar
    if progress_bar is None:
        progress_bar = tqdm(total=stream.filesize, unit='B', unit_scale=True, desc="Downloading Video")
    progress_bar.update(len(chunk))

url = input("Enter the video url: ")

my_proxies = {}

# Youtube object with inputted url
yt = YouTube(
    url,
    on_progress_callback=progress_function,
    proxies=my_proxies,
)

# Downloading video
stream = yt.streams.first()
stream.download(output_path='./downloads')
if progress_bar:
    progress_bar.close()

# Downloading captions
caption = yt.captions.get('en')
if not caption:
    caption = yt.captions.get('a.en')

if caption:
    print("Downloading Captions")
    caption_convert_to_srt = caption.generate_srt_captions()
    caption_convert_to_srt = caption_convert_to_srt.replace("\n\n", "\n")

    with open(os.path.join('./downloads', f"{yt.title}.srt"), "w", encoding="utf-8") as file:
        file.write(caption_convert_to_srt)
    print(f"Captions saved to 'downloads/{yt.title}.srt'")
else:
    print("No English captions found for this video.")
    exit()