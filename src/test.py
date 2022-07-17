import numpy as np
import cv2 as cv

# blank = np.zeros((800,500,4), dtype='uint8')
# blank[:] = (0,255,0,0.1)
# cv.imshow('b',blank)
# cv.waitKey(1000)

face_cascade = cv.CascadeClassifier("haarcascade_frontalface_default.xml")
img = cv.imread("images.jpg")
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray,1.5)
for (x,y,w,h) in faces:
    cv.rectangle(img,(x,y),(x+w,y+h), (255,0,0),2)
cv.imshow("img",img)
cv.waitKey(0)