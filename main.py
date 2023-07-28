import csv
import datetime
import pyttsx3
import pyaudio
import speech_recognition as sr
import openai
import time
import random
import asyncio
from picoh import picoh
import threading
import cv2
import numpy as np
import os 
import pyttsx3


picoh.reset()
picoh.wait(1)
#import internal
import facedetect
id = facedetect.id

id = 0
engine = pyttsx3.init()

# Stop the engine and clear its buffer
engine.stop()
# Set OpenAI API key
openai.api_key = "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"

def speak(text):
    engine.say(text)
    engine.runAndWait()
    
def chatbot(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",        
        #prompt=user_input,
        # temperature=0.5,
        max_tokens=50,
        # n=1,
        # stop=None,
        # frequency_penalty=0,
        # presence_penalty=0,
        # best_of=1,
        # max_completions=1,
        # logprobs=0,
        # echo=False,
        messages = [
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content


def recognize_speech():
    picoh.say("You can ask me a question")
    r = sr.Recognizer()
    speech = sr.Microphone()
    with speech as source:
        r.adjust_for_ambient_noise(source)
        print("SpeakNow")
        audio = r.record(source, duration  = 5)
        print("Stop Listening")
    try:
        # Use Google Speech Recognition API to transcribe audio
        transcription = r.recognize_google(audio, language = 'en-IN')
        # print out the transcribed text
        print("You said: {}".format(transcription))
        return transcription
    except sr.UnknownValueError:
    	print("Google Speech Recognition could not understand audio")
     
def start_conversation(id):
    # get current timestamp
    welcome_messages_1 = ["Hello! ", "Namaste! ", "Hi there! ", "Welcome! "]
    welcome_messages_2 = ["good to see you", "nice to meet you!", "It's a pleasure to meet you!", "Glad to make your acquaintance!"]
    # Concatenate the welcome message, name, and nice to meet you message
    message = random.choice(welcome_messages_1) + " " + random.choice(welcome_messages_2)
    
    print(message)
    picoh.setSynthesizer('Azure',ID ="a91d912a0e8449a4995ba047757dd83c")
    picoh.AccessUri = "https://centralindia.api.cognitive.microsoft.com/sts/v1.0/issueToken"
    picoh.SynthesizeUri = "https://centralindia.tts.speech.microsoft.com/cognitiveservices/v1"
    picoh.setVoice("MadhurNeural","hi-IN")
    picoh.say(message)
    picoh.say("My name is Picoh.")
    picoh.say("Harey Krishna, Harey Krishna Krishna Krishna, Harey Harey. Harey Rama, Harey Rama Rama Rama, Harey Harey.", True,True)

    while True:
         print("You can ask me a question.")
         user_input = recognize_speech()
         print(f"your said, {user_input} ")
         print(user_input)
         if user_input is not None and any(word in user_input.lower() for word in ['nothing', 'stop','thanks', 'goodbye','bye', 'see you', 'take care', 'thank', 'thank you']):
             goodbye_messages = ['Goodbye! I hope you visit next time', 'Bye! see you again', 'We will meet you again!', 'Take care! ']
             goodbye_message = random.choice(goodbye_messages)
             print(goodbye_message)
             picoh.say(goodbye_message, True, True)
             # Add timestamp to goodbye
             timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
             chat_goodbye = [timestamp, user_input, goodbye_message]
             # Write good response to CSV file        
             
             break
         elif  user_input is None:
             timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
             # Add timestamp to ChatGPT response 
             message = [timestamp, "User", "None"]         
             # Write ChatGPT response to CSV file         
             
             user_input = recognize_speech()
         else:
             # Start speaking and recognition tasks concurrently
             #text = speak("your question is" + user_input)
             moving = False
             picoh.move(picoh.HEADTURN,5)
             picoh.move(picoh.EYETILT,7)
             picoh.move(picoh.HEADNOD,9)
             picoh.say('Your question is', True, True)
             picoh.say(user_input, True, True)
             moving = True         
             chat_gpt_response = chatbot(user_input)
             print("Chatbot response: " + chat_gpt_response)
             timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
             #engine.say(chat_gpt_response)
             #engine.runAndWait()
             picoh.say(chat_gpt_response, True, True)
             # Add timestamp to ChatGPT response 
             chat_gpt_row = [timestamp, user_input, chat_gpt_response]         
             # Write ChatGPT response to CSV file  
             print("--------------------------------------------------------------------")
    # # close the file
    # conversation_file.close()
    # picoh.wait(3)
    # picoh.close()
    # start_conversation(id)
    
print(id)
start_conversation(id)

