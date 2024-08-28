# Foreign-Whispers

## Sections

- [About](#about)
- [Example Outputs](#example)
- [How to Use](#usage)
- [Hugging Face Space](#space)
- [Coqui TOS](#tos)

## About <a id="about"></a>

Foreign Whispers is a tool designed to transform your video content by adding both spoken and written subtitles in Spanish, all while replicating the original voices. This powerful application harnesses cutting-edge AI technologies to provide a seamless and engaging viewing experience for diverse audiences.

- **Youtube Video Download:** Automatically downloads YouTube videos to use as input for subtitle and voice replication, making the process straightforward and efficient.

- **Speaker Diarization:** Leverages speaker diarization technology to accurately identify and separate different speakers in your video, ensuring precise voice replication and subtitle alignment.

- **Voice Cloning and Translation:** Clones voices and translates spoken content into Spanish, making your content accessible to Spanish-speaking audiences.

- **Video Compliation:** Integrates the translated audio and subtitles into the original video. This process ensures that the final output maintains the video’s original flow and visual coherence while incorporating the new language features. The tool manages transitions, synchronization, and overall presentation to deliver a final product.

### <ins> Approaches </ins>

- Audio stetching/shrinking

To match the video length, the script speeds up the audio in specific sections. This approach ensures that the translated speech fits within the given timestamps for each speaker's segment.

- Frame adding/deleting

To allow the voice playback to play naturally, the script determines time interval differences and triggers markers for additional frames that need to be inserted or removed.

### <ins> Issues </ins>

- Audio Speed

Adjusting audio speed can result in unnatural sound, making it hard to understand.

- Audio Artifacts

Background noise and model variability can introduce random audio artifacts, affecting the clarity and quality of the output.

## Example Outputs <a id="example"></a>

### Audio Speed Manipulation

https://github.com/user-attachments/assets/98b8c054-b45d-4fc3-95a3-005702de68f9

### Audio Speed + Frame Manipulation

https://github.com/user-attachments/assets/a4e57fcd-b4d1-4b4c-af32-236445a444ca

## How to use: <a id="usage"></a>

Before running the script, ensure you have Python installed on your machine. You can download Python from the [official website](https://www.python.org/downloads/). 

1. Clone the repository to your local machine

```
git clone https://github.com/RobCaamano/foreign-whispers.git
```

2. Navigate to the project directory and download 'requirements.txt'. It is recommended to do this in a virtual environment. For information about creating and using conda environments, visit their [site](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html).

```
cd '[path to dir]'
pip install -r requirements.txt
```

3. This script is best used with a GPU for acceleration. To do this, you need to have a GPU with CUDA support and the appropriate CUDA toolkit installed. Follow the [CUDA installation guide](https://docs.nvidia.com/cuda/cuda-installation-guide-microsoft-windows/index.html) for details.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Note:** The time required for the script to complete depends on the computational power of your GPU.

4. Run the script in your virtual environment, providing the url through command line argument

```
python ./main.py "[url]"
```

## Hugging Face Space <a id="space"></a>

Our [Hugging Face Space](https://huggingface.co/spaces/Samin-Rob/FOREIGN-WHISPERS) provides an accessible interface for experimenting with our models. Please note that this space is configured to run on CPU rather than GPU. For optimal performance and faster processing, we recommend cloning the repository and running the models locally on your own hardware.

## Coqui Terms of Service <a id="tos"></a>

By using this project, you agree to the [Coqui Terms of Service](https://coqui.ai/cpml.txt).
