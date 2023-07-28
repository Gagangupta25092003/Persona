import wave
import numpy as np
import sys
import matplotlib.pyplot as plt
from pydub import AudioSegment

sound = AudioSegment.from_mp3("speech.mp3")
sound.export("wvfile.wav", format="wav")

w = wave.open("wvfile.wav", "r")












for i in range(0, len(raw)):
    
plt.plot(raw, color="blue")
plt.ylabel("Amplitude")

plt.show()