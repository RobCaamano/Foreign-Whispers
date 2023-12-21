import gradio as gr
from main import main as process_video

 # Runs main processing function
def run_pipeline(youtube_url):
   
    # Save final video path
    final_video_path = process_video(youtube_url)
    
    return final_video_path

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown(
        """
           # Convert YouTube video to speech and writen subtitles in Spanish, cloning speaker's voices.
           ## Note: This code is optimized for GPU. Online use is slow due to CPU. Recommended local usage.
        """,
        elem_id="header",
    )
    with gr.Column():
        user_prompt = gr.Textbox(
            placeholder="Enter YouTube Video URL here...",
        )
        btn = gr.Button("Convert")

    with gr.Column():
        generated_video = gr.Video(
            interactive=False, label="Generated Video", include_audio=True
        )

    btn.click(
        fn=run_pipeline,
        inputs=user_prompt,
        outputs=generated_video
    )

if __name__ == "__main__":
    demo.launch(show_error=True)
