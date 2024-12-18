# Open Video Translator

A tool box that can be used to download and translate almost any video to any language. 
It will be all **local** and **open-source**. 
With LLMs supporting long context, translation of each line of subtitle will be context aware. 

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) is used to download the video ([supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)). 
- [openai-whisper](https://github.com/openai/whisper) is used to transcribe the video ([supported languages](https://github.com/openai/whisper/blob/main/whisper/tokenizer.py)). 
- [ollama](https://github.com/ollama/ollama-python) is used to translate the video. Supported languages can vary from the model you chose. You shall refer to the respective model page for the supported languages. 

## Installation

I am assuming you have a NVIDIA GPU and you have installed the NVIDIA drivers. 
I am running on Ubunbu under Windows Subsystem Linux, so my set up might be a bit different. 

```bash
sudo apt update -y 
sudo apt upgrade -y 
sudo apt insall ffmpeg

conda create -n video-translation python=3.12.4
conda activate video-translation
conda install pytorch torchvision torchaudio pytorch-cuda=12.4 -c pytorch -c nvidia
pip install faster_whisper
conda install cudnn # you might need this for faster_whisper
conda isntall transformers 
```

<!-- Clone this repository. I am using docker that I don't need to worry about all the environment issues. Build the docker image by running the following command:

```bash
docker compose up
```

This will setup the environment and install all the dependencies.

In addition, make sure you have Ollama installed on your host machine. If not, please visit [Download Ollama](https://ollama.com/download). You could also install it in the docker container, but I found it makes more sense to have it installed on the host machine as you probably want to use it for other projects as well. 

After you have installed Ollama, you need to download the model. Use the following command to download the model:

```bash
ollama pull <model-name>
```

For a list of available models, please visit [Ollama Models](https://ollama.com/models).

## Usage 

Please refer to the notebook [example.ipynb](example.ipynb) for an example on how to use the tool box.

## Things you could customize 

- Use different OpenAI Whisper models. 
- Use different LLMs that can be run through Ollama. 
- Change the system prompt for translation. 
  - Provide a glossary for more accurate translation.
  - Tune the tone of voice for the translation. 
  - change the context length of the LLM.


## Additional help 

- If you docker does not detect you have a NVIDIA GPU, you can refer to my blog post [here](https://minhao-zhang.github.io/2024-11-07-docker-as-vm/) on setting up docker for deep learning on Windows.


- If you wish to use the AI summarization feature, you might need a long context LLM. All Ollama models defaults to 2k context length. You can create a new model by creating a file called `modelfile` with 

    ```text 
    FROM <model-name>
    PARAMETER num_ctx <context-length>
    ```

    You can pick any model you wish to use and set the context length to any value you wish. The default is 2048, so you probably want to set it to a larger value. A good rule of thumb is that normal speech is about 140 words per minute, 4 tokens for 3 words. So for a 10 minute video, a 2k context is needed. In addition, there will be some overhead from the system prompt so you always want to be on the safe side. 

    After you have created the `modelfile`, you can create a new model by running the following command:

    ```bash
    ollama create your-long-context-model-name -f modelfile
    ```

    You now have your own model with a larger context length. -->