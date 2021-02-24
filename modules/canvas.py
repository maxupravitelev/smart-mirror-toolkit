from threading import Thread
import cv2
import json
import time
import numpy as np
import os
import glob

# function to parse bool value from config file
from utils.boolcheck import boolcheck

class Canvas_painter:
    def __init__(self, cap_dimensions=[640,480]):
        
        # get settings from config file
        config_path = 'config/config.json'

        with open(config_path) as config_file:
            config = json.load(config_file)

        # check if image folder exist, create if it doesn't
        folder_path = 'images'
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)
        
        # count files in folder for creating continuous filenames
        self.files_in_folder = 0
        for path in glob.glob(folder_path + "*.jpg"):
            self.files_in_folder += 1

        # init thread handling
        self.stopped = False

        # set verbose mode
        self.verbose = boolcheck(config["general_config"]["verbose"])

        self.frame_width = 1024
        self.frame_height = 768

        self.resize_width_factor = self.frame_width / cap_dimensions[0]
        self.resize_heigth_factor = self.frame_height / cap_dimensions[1]
        self.resize_factors = [self.resize_width_factor, self.resize_heigth_factor]

        self.black_frame = np.zeros((self.frame_height, self.frame_width, 3), np.uint8)
        self.navigation_frame = np.zeros((self.frame_height, self.frame_width, 3), np.uint8)
        self.combined_frame = np.zeros((self.frame_height, self.frame_width, 3), np.uint8)
        
        self.reset_area_width = 50
        self.reset_area_height = 50

        self.save_area_width = 100
        self.save_area_height = 100
        self.save_area_y = self.frame_height - self.save_area_height

        self.painter_brush_x = 0
        self.painter_brush_y = 0

        self.file_counter = 0

        self.reset_canvas()

    def reset_canvas(self):
        cv2.rectangle(self.black_frame, (0, 0), (self.frame_width, self.frame_height), (0, 0, 0), -1)
        cv2.rectangle(self.navigation_frame, (0, 0), (self.reset_area_width, self.reset_area_height), (10, 10, 10), -1)
        cv2.rectangle(self.navigation_frame, (0, self.save_area_y), (self.save_area_width, self.save_area_y + self.save_area_height), (120, 120, 120), -1)

            
    def start(self):    
        Thread(target=self.paint, args=()).start()
        return self    

    def paint(self):
        while not self.stopped:
            if self.painter_brush_x < self.reset_area_width and self.painter_brush_y < self.reset_area_height:
                self.reset_canvas()
                time.sleep(1)

            if self.painter_brush_x < self.save_area_width and self.painter_brush_y > self.save_area_y:
                self.files_in_folder += 1
                localPath = 'images/image1000'+str(self.files_in_folder)+'.jpg'
                cv2.imwrite(localPath,self.black_frame)
                time.sleep(1)


            

            # if cv2.waitKey(1) == ord("q"):
            #     if self.verbose == True:
            #         print("painter stopped")
            #     self.stopped = True

    def stop(self):
        self.stopped = True