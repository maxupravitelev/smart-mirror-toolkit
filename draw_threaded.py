import cv2
import numpy as np
import time
import json
from modules.painter import Painter
from modules.canvas import Canvas_painter

# function to parse bool value from config file
from utils.boolcheck import boolcheck


# get settings from config file
config_path = 'config/config.json'

with open(config_path) as config_file:
    config = json.load(config_file)

## mode selection
enable_fps_timer = boolcheck(config["general_config"]["enable_fps_timer"])


camera_mode = "webcam"

# init videostream (separate thread)
if camera_mode == "webcam":

    # start raspivid in a subprocess
    # import subprocess
    # cmd = "raspivid -n -t 0 -n  -w 1024 -h 768  -ih -fl -l -o - | /bin/nc -lvp 5000"
    # subprocess.Popen(cmd, shell=True)
    from modules.cam import VideoStream
    time.sleep(2)
    cap = VideoStream(src=0).start()
else: 
    from modules.PiCam import PiCam 
    cap = PiCam().start()


# cap = cv2.VideoCapture(0)
# # Set camera resolution

# cap_width = 480
# cap_height = 320
# cap.set(3, cap_width)
# cap.set(4, cap_height)

cap_width = cap.stream.get(3)
cap_height = cap.stream.get(4)


cap_dimensions = [cap_width, cap_height]

canvas = Canvas_painter(cap_dimensions).start()
#canvas.reset_canvas()

time.sleep(1.0)
#_, black_frame = cap.read()


# frame_width = 640
# frame_height = 480

# resize_width_factor = frame_width / cap_width
# resize_heigth_factor = frame_height / cap_height
# resize_factors =  [resize_width_factor, resize_heigth_factor]

# black_frame = np.zeros((frame_height, frame_width, 3), np.uint8)
# print(frame_width)
# print(frame_height)

# cv2.rectangle(black_frame, (0, 0), (frame_width, frame_height), (0, 0, 0), -1)


if enable_fps_timer == True:
    timer2 = time.time()

# reset_area_width = 50
# reset_area_height = 50
# save_area_width = 50
# save_area_height = 50
# save_area_y = frame_height - 50

# def reset_canvas():
#     cv2.rectangle(black_frame, (0, 0), (frame_width, frame_height), (0, 0, 0), -1)
#     cv2.rectangle(black_frame, (0, 0), (reset_area_width, reset_area_height), (10, 10, 10), -1)
#     cv2.rectangle(black_frame, (0, save_area_y), (save_area_width, save_area_y + save_area_height), (20, 20, 20), -1)

# reset_canvas()

painter = Painter(canvas.black_frame, canvas.resize_factors).start()


counter = 0

while True:

    if enable_fps_timer == True:
        timer1 = time.time()

    frame = cap.read()
    frame = cv2.flip(frame, 1)

    painter.frame = frame

    #black_frame = canvas.black_frame
    navigation_frame = canvas.navigation_frame

    cv2.circle(canvas.black_frame, (painter.brush_x, painter.brush_y), painter.brush_radius, (255, 255, 255), -1)

    canvas.painter_brush_x = painter.brush_x
    canvas.painter_brush_y = painter.brush_y
    
    if enable_fps_timer == True:
        print("FPS: " + str(1/((timer1-timer2))))
        timer2 = time.time()

    combined_frame = cv2.addWeighted(canvas.black_frame,1,navigation_frame,1,0)

    cv2.imshow("Frame", combined_frame)
    key = cv2.waitKey(1)
    
    if key == 27:
        break
    
cap.release()
cv2.destroyAllWindows()

