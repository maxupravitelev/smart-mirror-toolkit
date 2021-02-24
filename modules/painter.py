from threading import Thread
import cv2
import imutils
import json
import time
import numpy as np

# function to parse bool value from config file
from utils.boolcheck import boolcheck

class Painter:
    def __init__(self, frame, resize_factors):
        
        # get settings from config file
        config_path = 'config/config.json'

        with open(config_path) as config_file:
            config = json.load(config_file)

        self.frame = frame

        # init thread handling
        self.stopped = False

        # set verbose mode
        self.verbose = boolcheck(config["general_config"]["verbose"])

        # red color
        self.low_red = np.array([161, 100, 84])
        self.high_red = np.array([179, 255, 255])

        self.brush_x = 0
        self.brush_y = 0
        self.brush_radius = 0

        self.resize_width_factor = resize_factors[0]
        self.resize_heigth_factor = resize_factors[1]

        self.resize_width = 200
        
    def start(self):    
        Thread(target=self.paint, args=()).start()
        return self    

    def paint(self):
        counter = 0
        while not self.stopped:

            # Source for color detection: # https://pysource.com/2019/06/05/control-webcam-with-servo-motor-and-raspberry-pi-opencv-with-python/ 
            resized_frame = imutils.resize(self.frame, self.resize_width)

            hsv_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2HSV)
            red_mask = cv2.inRange(hsv_frame, self.low_red, self.high_red)

            contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
            contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
            resized_frame_height = resized_frame.shape[0]
            resize_factor_height_finding_contours = self.frame.shape[0] / resized_frame_height
            resize_factor_width_finding_contours = self.frame.shape[1] / self.resize_width 
            # print(red_mask.shape)
            # if len(contours ) > 0:
            #     x, y, w, _ = cv2.boundingRect(contours[0])
            #     self.brush_x = int(x * self.resize_width_factor)
            #     self.brush_y = int(y * self.resize_heigth_factor)
            #     self.brush_radius = int((w / 10) * self.resize_width_factor)

            for cnt in contours:
                if cv2.contourArea(cnt) > 100:
                    (x, y, w, _) = cv2.boundingRect(cnt)
                    self.brush_x = int(x * self.resize_width_factor * resize_factor_width_finding_contours)
                    self.brush_y = int(y * self.resize_heigth_factor * resize_factor_height_finding_contours)
                    self.brush_radius = int((w / 10) * self.resize_width_factor * resize_factor_width_finding_contours)

                    break

            # counter += 1
            # print(counter)
            # if cv2.waitKey(1) == ord("q"):
            #     if self.verbose == True:
            #         print("painter stopped")
            #     self.stopped = True

    def stop(self):
        self.stopped = True