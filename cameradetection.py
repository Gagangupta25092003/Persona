import cv2
import numpy as np

face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
vid = cv2.VideoCapture(0)

while True:
    
    _, frame = vid.read()#reads the current frame to the variable frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#converts frame -> grayscaled image
    faces = face_cascade.detectMultiScale(gray, minSize=(80, 80), minNeighbors=3)
    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)#draws a rectangle around the face
        Xpos = x+(w/2)#calculates the X co-ordinate of the center of the face.
        Ypos = y+(h/2)
        
        print(Xpos)