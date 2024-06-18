
### General imports ###
from __future__ import division
import numpy as np
import pandas as pd
import time
import re
import os
from collections import Counter
import altair as alt

### Flask imports
import requests
from flask import Flask, render_template, session, request, redirect, flash, Response

### Audio imports ###
from library.speech_emotion_recognition import *

import requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "audio")

data= response.json()
print (data)

path = data['1']['path']
audio = data['1']['audio'] 

print (path)
print (audio)




# Sub dir to speech emotion recognition model
model_sub_dir = os.path.join('Models', 'audio.hdf5')

# Instanciate new SpeechEmotionRecognition object
SER = speechEmotionRecognition(model_sub_dir)

# Voice Record sub dir
#rec_sub_dir = os.path.join('tmp','voice_recording.wav')
rec_sub_dir = os.path.join(path,audio)
print(rec_sub_dir)

# Predict emotion in voice at each time step
step = 1 # in sec
sample_rate = 16000 # in kHz
emotions, timestamp = SER.predict_emotion_from_file(rec_sub_dir, chunk_step=step*sample_rate)

# Export predicted emotions to .txt format
SER.prediction_to_csv(emotions, os.path.join("static/js/db", "audio_emotions.txt"), mode='w')
SER.prediction_to_csv(emotions, os.path.join("static/js/db", "audio_emotions_other.txt"), mode='a')

# Get most common emotion during the interview
major_emotion = max(set(emotions), key=emotions.count)

# Calculate emotion distribution
emotion_dist = [int(100 * emotions.count(emotion) / len(emotions)) for emotion in SER._emotion.values()]

# Export emotion distribution to .csv format for D3JS
df = pd.DataFrame(emotion_dist, index=SER._emotion.values(), columns=['VALUE']).rename_axis('EMOTION')
df.to_csv(os.path.join('static/js/db','audio_emotions_dist.txt'), sep=',')

# Get most common emotion of other candidates
df_other = pd.read_csv(os.path.join("static/js/db", "audio_emotions_other.txt"), sep=",")

# Get most common emotion during the interview for other candidates
major_emotion_other = df_other.EMOTION.mode()[0]

# Calculate emotion distribution for other candidates
emotion_dist_other = [int(100 * len(df_other[df_other.EMOTION==emotion]) / len(df_other)) for emotion in SER._emotion.values()]

# Export emotion distribution to .csv format for D3JS
df_other = pd.DataFrame(emotion_dist_other, index=SER._emotion.values(), columns=['VALUE']).rename_axis('EMOTION')
df_other.to_csv(os.path.join('static/js/db','audio_emotions_dist_other.txt'), sep=',')

# Sleep
time.sleep(0.5)

print (major_emotion)
#print (major_emotion_other)
print (emotion_dist)
#print (emotion_dist_other)

#return major_emotion, major_emotion_other, emotion_dist, emotion_dist_other
PARAMS = {"major_emotion": major_emotion, 
                "Happy":emotion_dist[0], "Satisfied":emotion_dist[1], 
                "Interested":emotion_dist[2], "Neutral":emotion_dist[3], 
                "Angry":emotion_dist[4], "Unsatisfied":emotion_dist[5], "Unhappy":emotion_dist[6]
         
         }
#self._emotion = {0:'Happy', 1:'Satisfied', 2:'Interested', 3:'Neutral', 4:'Angry', 5:'Unsatisfied', 6:'Unhappy'}

r = requests.post(BASE + "result/1", PARAMS)
d= r.json()
print (d)