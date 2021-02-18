# built upon: https://github.com/jrosebr1/imutils/blob/master/imutils/video/pivideostream.py

from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
# import cv2

# import numpy as np



class PiCam:
    def __init__(self, resolution=(640, 480)):
        # initialize the camera

        # self.update_values()

        self.frame = None

        # init thread
        self.stopped = False

        self.camera = PiCamera() 

        # set resolution
        #self.camera.resolution = (1024, 768)
        
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,
            format="bgr", use_video_port=True)
        
        self.picam_fully_stopped = False

    # def update_values(self):

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        for f in self.stream:

            # if the thread indicator variable is set, stop the thread
            # and resource camera resources
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return

            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.frame = f.array

            self.rawCapture.truncate(0)



    def read(self):
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True