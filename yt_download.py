import argparse
from pytube import YouTube
from tqdm import tqdm
import os

def download_youtube_video(video_url, download_captions=False):
    progress_bar = None

    # Updates progress bar
    def progress_function(stream, chunk, bytes_remaining):
        nonlocal progress_bar
        if progress_bar is None:
            progress_bar = tqdm(total=stream.filesize, unit='B', unit_scale=True, desc="Downloading Video")
        current = stream.filesize - bytes_remaining
        progress_bar.n = current
        progress_bar.last_print_n = current
        progress_bar.update()

    if not os.path.exists('./downloads'):
        os.makedirs('./downloads')

    # Youtube object with inputted url
    yt = YouTube(
        video_url,
        on_progress_callback=progress_function,
    )

    # Downloading video
    stream = yt.streams.get_highest_resolution()
    stream.download(output_path='./downloads')
    if progress_bar:
        progress_bar.close()

    # Download captions (default=disabled)
    if download_captions:
        caption = yt.captions.get('en') or yt.captions.get('a.en')
        if caption:
            caption_convert_to_srt = caption.generate_srt_captions()
            caption_convert_to_srt = caption_convert_to_srt.replace("\n\n", "\n")
            with open(os.path.join('./downloads', f"{yt.title}.srt"), "w", encoding="utf-8") as file:
                file.write(caption_convert_to_srt)
            print(f"Captions saved to 'downloads/{yt.title}.srt'")
        else:
            print("No English captions found for this video.")

# Driver function
def download_video(url, download_captions=False):
    video_path = './downloads/' + YouTube(url).streams.get_highest_resolution().default_filename
    download_youtube_video(url, download_captions)
    return video_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download YouTube video and captions")
    parser.add_argument("video_url", help="YouTube video URL")
    parser.add_argument("--captions", action="store_true", help="Download captions if available")
    args = parser.parse_args()

    download_video(args.video_url, args.captions)