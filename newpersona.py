import speech_recognition as sr
from pyfirmata import Arduino, SERVO, util
from time import sleep
import openai
from gtts import gTTS
from playsound import playsound
import cv2
import numpy as np
import threading
import wave
from pydub import AudioSegment
import urllib.request

##############################################################

r = sr.Recognizer()
mic = sr.Microphone()

##############################################################

openai.api_key = "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"
modelengine = "text-davinci-003"
##############################################################

port = '/dev/ttyUSB0'
board = Arduino(port)
##############################################################

face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
url = "http://192.168.177.14/400x296.jpg"
##############################################################


pinMouth = 8
pinEyeX = 4
pinEyeY = 3
pinNeck = 6
pinLEDRed1 = 13
pinLEDRed2 = 12
pinLEDBlue1 = 10
pinLEDBlue2 = 11
NeckPos = 75
EyeYPos = 40
thread_bool = True
f = []
##############################################################

def LedBlue(x):
    board.digital[pinLEDBlue1].write(x)
    board.digital[pinLEDBlue2].write(x)
##############################################################

def LedRed(x):
    board.digital[pinLEDRed1].write(x)
    board.digital[pinLEDRed2].write(x)   
##############################################################

board.digital[pinMouth].mode = SERVO
board.digital[pinEyeX].mode = SERVO
board.digital[pinEyeY].mode = SERVO
board.digital[pinNeck].mode = SERVO
LedBlue(1)
LedRed(1)

##############################################################

def lipsync():
    global f
    global pinMouth
    print(",dfmsnbvkjdsf lsd")
    for k in f:    
        y = int((k)*40)
        board.digital[pinMouth].write(y)
        print(y)
        sleep(0.05)
    
##############################################################

def moveEyeX():
    while True:
        board.digital[pinEyeX].write(30)
        sleep(0.5)
        board.digital[pinEyeX].write(65)
        sleep(0.5)
        print("jhsv")

##############################################################
    
def neckRotate(pos):
    if(NeckPos < pos):
        pos = min(pos, 150)
        for i in range(NeckPos, pos):
            board.digital[NeckPos].write(i)
            sleep(0.01)
        NeckPos = pos    
    else:
        pos = max(0,pos)
        for i in range(pos, NeckPos):
            board.digital[NeckPos].write(i)
        
        NeckPos = pos 
        
##############################################################

def moveEyeY():
    while True:
        board.digital[pinEyeX].write(10)
        sleep(0.5)
        board.digital[pinEyeX].write(60)
        sleep(0.5)
        print("jhsv")
    
##############################################################

def moveNeck():
    while True:
        for i in range(0,150):
            board.digital[pinNeck].write(i);
            sleep(0.02)
        for i in range(150,0, -1):
            board.digital[pinNeck].write(i);
            sleep(0.02)
    
##############################################################

def rotateEye():
    board.digital[pinEyeX].write(30)
    board.digital[pinEyeY].write(35)
    for i in range(-17.5,17.5):
        j = (1-(i*i/(17.5*17.5)))*25*25
        
        x = (int)(i + 47.5)
        y = (int)(j + 35)
    
    board.digital[pinEyeX].write(47.5)
    board.digital[pinEyeY].write(35)  
        
        
##############################################################

def orientation():
    global EyeYPos
    global NeckPos
    global pinEyeY
    global pinNeck
    global thread_bool
    while thread_bool:
        
        imgResponse = urllib.request.urlopen(url)
        imgnp = np.array(bytearray(imgResponse.read()),dtype=np.uint8)
        img = cv2.imdecode(imgnp, -1)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        face= face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=2)
        x1 = -1;
        y1 = -1;
        w1 = -1;
        h1 = -1;
        for x,y,w,h in face:
            if(w*h > w1*h1):
                w1 = w
                h1 = h
                x1 = x
                y1 = y
           
        
        
        if x1 != -1:
            Xpos = x1+(w1/2)#calculates the X co-ordinate of the center of the face.
            Ypos = y1+(h1/2)
            y1= int((Ypos)*(0.169)+10)
            x1 = int(((Xpos)*0.225*-1 + 120))
            if x1 >  NeckPos:
                for i in range(NeckPos, x1):
                    board.digital[pinNeck].write(i)
                    sleep(0.01)
                NeckPos = x1
            else:
                for i in range(NeckPos, x1, -1):
                    board.digital[pinNeck].write(i)
                    sleep(0.01)
                NeckPos = x1
            
            # if y > EyeYPos:
            #     for i in range(EyeYPos, y):
            #         board.digital[pinEyeY].write(i)
            #         sleep(0.01)
            #     EyeYPos = y
            # else:
            #     for i in range(EyeYPos, y, -1):
            #         board.digital[pinEyeY].write(i)
            #         sleep(0.01)
            #     EyeYPos = y
                
##############################################################

def interaction():
    global f
    while True:      
        with mic as source:
            r.adjust_for_ambient_noise(source)        
            print("LISTENING.........")
            LedBlue(0)
            LedRed(1)
            audio = r.listen(source)
            LedRed(0)
            LedBlue(1)
            said = r.recognize_google(audio).lower()
            LedRed(1)
            LedBlue(1)
            print(said)
            completion = openai.Completion.create(
            engine = modelengine,
            prompt = said,
            max_tokens = 50,
            n = 1,
            stop = None,
            temperature = 0.5,
            )
            print("Output:")
            response = completion.choices[0].text
            print(response)
            tts  = gTTS(response)
            tts.save("speech.mp3")
            
            sound = AudioSegment.from_mp3("speech.mp3")
            sound.export("wvfile.wav", format="wav")
            w = wave.open("wvfile.wav", "rb")
            
            raw = w.readframes(-1)
            raw = np.frombuffer(raw, 'int16')
            raw = abs(raw)
            mx = max(raw)
            raw = raw/mx
            
            f = []
            for i in range(0, len(raw), 1200):
                k= 0
                for j in range(i, min(i+1200, len(raw))):
                    k = max(k, raw[j])
                f.append(k)
            thread_lipsync = threading.Thread(target = lipsync)
            thread_lipsync.start()
            playsound("speech.mp3")
            print("jdvn")
            thread_lipsync.join()
            if said == "close persona":
                break
    
            
##############################################################  
    

thread_orientation = threading.Thread(target=orientation)
thread_interaction = threading.Thread(target=interaction)

##############################################################

board.digital[pinMouth].write(0)
board.digital[pinNeck].write(75)
NeckPos = 75
board.digital[pinEyeY].write(35)
board.digital[pinEyeX].write(47.5)
thread_orientation.start()
thread_interaction.start()



    