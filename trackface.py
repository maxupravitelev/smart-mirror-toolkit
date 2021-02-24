import cv2
import numpy as np


cap = cv2.VideoCapture(0)

# Set camera resolution
cap.set(3, 1024)
cap.set(4, 768)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

_, black_frame = cap.read()
# cv2.rectangle(black_frame, (0, 0), (1, 1), (255, 0, 0), 2)

frame_width = int(cap.get(3)) 
frame_height = int(cap.get(4))
print(frame_width)
print(frame_height)

def trackface(frame):
    cv2.rectangle(black_frame, (0, 0), (frame_width, frame_height), (0, 0, 0), -1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 10)

    for (x, y, w, h) in faces:
        cv2.rectangle(black_frame, (x, y), (x+w, y+h), (255, 255, 255), 5)

    return black_frame

while True:
    _, frame = cap.read()
 
    frame = cv2.flip(frame, 1)

    frame = trackface(frame)

    #cv2.namedWindow('frame', cv2.WINDOW_FREERATIO)
    #cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    cv2.imshow("frame", frame)
    key = cv2.waitKey(1)
    
    if key == 27:
        break
    
cap.release()
cv2.destroyAllWindows()

# Built upon: https://pysource.com/2019/06/05/control-webcam-with-servo-motor-and-raspberry-pi-opencv-with-python/