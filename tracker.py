import cv2
import numpy as np
import time
import argparse

# function to parse bool value from config file
from utils.boolcheck import boolcheck


## parse args from command line
parser = argparse.ArgumentParser()
parser.add_argument("--track", type=str, default="face",
        help="choose tracking mode")
parser.add_argument("--gpio", type=str, default="False",
        help="enable gpio motor")  
parser.add_argument("--fullscreen", type=str, default="False",
        help="enable fullscreen mode") 
args = vars(parser.parse_args())
fullscreen = boolcheck(args["fullscreen"])
track = args["track"]
gpio = boolcheck(args["gpio"])

# init motor if set
if gpio == True:
    from modules.gpio_motor import GPIO_motor
    motor = GPIO_motor()

# init capture
cap = cv2.VideoCapture(0)
time.sleep(1)

# Set camera resolution
cap.set(3, 1024)
cap.set(4, 768)

# load face model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# init frame
_, canvas = cap.read()

frame_width = int(cap.get(3)) 
frame_height = int(cap.get(4))
print("Frame dimensions: " + str((frame_width, frame_height)))

# get middle of the frame for moving the motor left or right according to x coordinates of detected objects
middle_of_frame_x = int(frame_width / 2)


# function for detecting and tracking faces
def trackface(frame):
    cv2.rectangle(canvas, (0, 0), (frame_width, frame_height), (0, 0, 0), -1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 10)

    x = middle_of_frame_x

    for (x, y, w, h) in faces:
        cv2.rectangle(canvas, (x, y), (x+w, y+h), (255, 255, 255), 5)

    return canvas, x


# function for detecting and tracking color
def trackcolor(frame):
    
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define color limits to be detected 
    # red color
    low_color_limit = np.array([161, 155, 84])
    high_color_limit = np.array([179, 255, 255])

    color_mask = cv2.inRange(hsv_frame, low_color_limit, high_color_limit)
    
    # print(red_mask)
    contours, _ = cv2.findContours(color_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)

    cv2.rectangle(frame, (0, 0), (frame_width, frame_height), (0, 0, 0), -1)

    for cnt in contours:
        if cv2.contourArea(cnt) > 1000:
            (x, y, w, h) = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 3)
            
            break
        
    return frame, x


# function for moving gpio motor on a raspberry pi
def move_gpio_motor(x):
    if x < middle_of_frame_x:
        print("left")
        motor.move_non_threaded(1, "left")
        #time.sleep(0.1)
    elif x == middle_of_frame_x:
        print("stay")
    else:
        print("right")
        motor.move_non_threaded(1, "right")
        #time.sleep(0.1)


# main loop
while True:
    _, frame = cap.read()
 
    frame = cv2.flip(frame, 1)

    if track == "face":
        frame, x = trackface(frame)
    if track == "color":
        frame, x = trackcolor(frame)

    if gpio == True:
        move_gpio_motor(x)

    # enable fullscreen mode
    if fullscreen == True:
        cv2.namedWindow('frame', cv2.WINDOW_FREERATIO)
        cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    cv2.imshow("frame", frame)
    key = cv2.waitKey(1)
    
    if key == 27:
        break
    
cap.release()
cv2.destroyAllWindows()

# Built upon: https://pysource.com/2019/06/05/control-webcam-with-servo-motor-and-raspberry-pi-opencv-with-python/