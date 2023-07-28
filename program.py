import speech_recognition as sr
from pyfirmata import Arduino, SERVO, util
import time
import openai
from gtts import gTTS
from playsound import playsound

##############################################################

r = sr.Recognizer()
mic = sr.Microphone()

##############################################################

openai.api_key = "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"
modelengine = "text-davinci-003"
##############################################################

port = '/dev/ttyUSB0'
board = Arduino(port)
print(board.get_firmata_version)
##############################################################

pinMouth = 5
pinEyeX = 4
pinEyeY = 3
pinNeck = 6
pinLEDRed = 13
pinLEDBlue = 12
##############################################################

board.digital[pinMouth].mode = SERVO
board.digital[pinEyeX].mode = SERVO
board.digital[pinEyeY].mode = SERVO
board.digital[pinNeck].mode = SERVO
board.digital[pinLEDRed].write(1)
board.digital[pinLEDBlue].write(1)

##############################################################

def moveall():
    k1 = 0
    k2 = 0
    k3 = 30
    board.digital[pinEyeX].write()
##############################################################

def movemouth(start, end, t):
    for i in range(start, end):
        board.digital[pinMouth].write(i)
        time.sleep(t/abs(end-start))
##############################################################

def setServo(angle, pinNo):
    board.digital[pinNo].write(angle)
############################################################## 
   
def moveEyeTranslation(Xstart, Xend, Ystart, Yend, t):
    increment = (Yend-Ystart)/abs(Xend-Xstart)
    for i in range(Xstart, Xend):
        board.digital[pinEyeX].write(i)
        board.digital[pinEyeY].write(j)
        j+= increment
        time.sleep(t/(Xstart-Xend))
##############################################################

moveall()
try:
    while True:
        with mic as source:
            r.adjust_for_ambient_noise(source)        
            print("LISTENING.........")
            board.digital[pinListeningLED].write(1)
            audio = r.listen(source)
            board.digital[pinListeningLED].write(0)
            board.digital[pinReplyingLED].write(1)
            said = r.recognize_google(audio)
            said = said.lower()
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
            playsound("speech.mp3")
            try:
                    if said == 'hello bot':
                        moveall()
                                            
                    elif 'move your mouth' in said:
                        movemouth(75, 0, 0.5)
                        movemouth(0, 75, 0.5)
            except:
                    print("Error in Listening")
            
            board.digital[pinReplyingLED].write(0)
except:
    print("Program stopped")
    board.digital[pinListeningLED].write(0)
    board.digital[pinReplyingLED].write(0)