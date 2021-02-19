from threading import Thread
import cv2
import imutils
import json
import time
import numpy as np

# function to parse bool value from config file
from utils.boolcheck import boolcheck

class Painter:
    def __init__(self, frame):
        
        # set setting from config file
        config_path = 'config/config.json'

        with open(config_path) as config_file:
            config = json.load(config_file)

        self.frame = frame

        # init thread handling
        self.stopped = False

        # set verbose mode
        self.verbose = boolcheck(config["general_config"]["verbose"])

        # red color
        self.low_red = np.array([161, 155, 84])
        self.high_red = np.array([179, 255, 255])

        self.brush_x = 0
        self.brush_y = 0
        
    def start(self):    
        Thread(target=self.analyze, args=()).start()
        return self    

    def analyze(self):
        while not self.stopped:

            # Source for color detection: # https://pysource.com/2019/06/05/control-webcam-with-servo-motor-and-raspberry-pi-opencv-with-python/ 
            hsv_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
            red_mask = cv2.inRange(hsv_frame, self.low_red, self.high_red)

            contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
            contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)

            for cnt in contours:
                # if cv2.contourArea(cnt) > 1000:
                    (x, y, _, _) = cv2.boundingRect(cnt)
                    self.brush_x = x
                    self.brush_y = y

                    break

            if cv2.waitKey(1) == ord("q"):
                if self.verbose == True:
                    print("painter stopped")
                self.stopped = True

    def set_background(self, image):
        self.background_image = imutils.resize(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), self.resize_width)
        self.motion_detected = False

    def stop(self):
        self.stopped = True