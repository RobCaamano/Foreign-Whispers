# Foreign-Whispers

## Sections

- [About](#about)
- [Example Output](#example)
- [How to Use](#usage)
- [Hugging Face Space](#space)

## About <a id="about"></a>

Takes a video as input and outputs the same video with both spoken and written subtitles in Spanish, replicating each individual voice. Utilizes OpenAI Whisper, Opus NLP, Pyannote and xTTS models.

## Example Output Video <a id="example"></a>

https://github.com/RobCaamano/Foreign-Whispers/assets/65639885/e373b174-bbe4-4a35-ab07-fac2714fdf64

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

6. Run the script in your virtual environment

```
python ./main.py "[url]"
```

## Huggingface Space <a id="space"></a>

[link](https://huggingface.co/spaces/Samin-Rob/FOREIGN-WHISPERS)
