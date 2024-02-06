# -*- coding: utf-8 -*-
"""Personal-Assistant.ipynb

Automatically generated by Colaboratory.

"""

pip install cohere

pip install tiktoken

"""# Installation"""

pip install openai

pip install openai

pip install kaleido

# Downloading all the dependencies
!pip install -q git+https://github.com/openai/whisper.git
!pip install -q gradio==3.50
!pip install -q openai
!pip install -q gTTS

"""# Imports"""

# Importing all the libraries
import whisper

import time
import warnings
import json
import openai
import os
from gtts import gTTS

"""# Defining Variables"""

!python -m json.tool /content/SECRET_KEY.json

!cat /content/SECRET_KEY.json

# Accessing the API key
with open('SecretKey.txt') as file:
  openai.api_key = file.read()

# Loading the modal
model = whisper.load_model("base")

# Checking if the model is using the GPU or not
model.device

!ffmpeg -f lavfi -i anullsrc=r=44100:cl=mono -t 10 -q:a 9 -acodec libmp3lame Temp.mp3

"""# API_Function"""

# Main API integration function
def chat_api(input_text):
    messages = [
    {"role": "system", "content": "You are a helpful assistant."}]

    if input_text:
        messages.append(
            {"role": "user", "content": input_text},
        )
        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )

    reply = chat_completion.choices[0].message.content
    return reply

"""# Transcribe Function"""

# This function takes the audio as the input and generates text and audio output
def transcribe(audio):

    language = 'en'

    audio = whisper.load_audio(audio)
    audio = whisper.pad_or_trim(audio)

    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    _, probs = model.detect_language(mel)

    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)
    result_text = result.text

    out_result = chat_api(result_text)

    audioobj = gTTS(text = out_result,
                    lang = language,
                    slow = False)

    audioobj.save("Temp.mp3")

    return [result_text, out_result, "Temp.mp3"]

"""# Gradio Interface"""

!pip install gradio==3.50
import gradio as gr

# Creating the UI for the WebApp
output_1 = gr.Textbox(label="Speech to Text")
output_2 = gr.Textbox(label="Assistant Output")
output_3 = gr.Audio("Temp.mp3")

gr.Interface(
    title = 'Personal Assistant',
    fn=transcribe,
    inputs=[
        gr.inputs.Audio(source="microphone", type="filepath")
    ],

    outputs=[
        output_1,  output_2, output_3
    ],
    live=True).launch(share=True, debug=True)



