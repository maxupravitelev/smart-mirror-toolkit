import cv2
import numpy as np
import time
import json
from modules.painter import Painter

# function to parse bool value from config file
from utils.boolcheck import boolcheck


# get settings from config file
config_path = 'config/config.json'

with open(config_path) as config_file:
    config = json.load(config_file)

## mode selection
enable_fps_timer = boolcheck(config["general_config"]["enable_fps_timer"])


# camera_mode = "picam"

# # init videostream (separate thread)
# if camera_mode == "webcam":

#     # start raspivid in a subprocess
#     import subprocess
#     cmd = "raspivid -n -t 0 -n  -w 1024 -h 768  -ih -fl -l -o - | /bin/nc -lvp 5000"
#     subprocess.Popen(cmd, shell=True)
#     from modules.cam import VideoStream
#     time.sleep(2)
#     cap = VideoStream(src=0).start()
# else: 
#     from modules.PiCam import PiCam 
#     cap = PiCam().start()


cap = cv2.VideoCapture(0)
# # Set camera resolution
cap.set(3, 640)
cap.set(4, 480)


time.sleep(1.0)
_, black_frame = cap.read()
# cv2.rectangle(black_frame, (0, 0), (1, 1), (255, 0, 0), 2)

frame_width = int(black_frame.shape[1]) 
frame_height = int(black_frame.shape[0])
print(frame_width)
print(frame_height)

cv2.rectangle(black_frame, (0, 0), (frame_width, frame_height), (0, 0, 0), -1)

painter = Painter(black_frame).start()

if enable_fps_timer == True:
    timer2 = time.time()

while True:


    if enable_fps_timer == True:
        timer1 = time.time()

    _, frame = cap.read()
    frame = cv2.flip(frame, 1)

    painter.frame = frame
    
    cv2.circle(black_frame, (painter.brush_x, painter.brush_y), painter.brush_radius, (255, 255, 255), -1)

    if enable_fps_timer == True:
        print("FPS: " + str(1/((timer1-timer2))))
        timer2 = time.time()

    cv2.imshow("Frame", black_frame)
    key = cv2.waitKey(1)
    
    if key == 27:
        break
    
cap.release()
cv2.destroyAllWindows()

