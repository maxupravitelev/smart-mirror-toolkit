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

cap_width = 480
cap_height = 320
cap.set(3, cap_width)
cap.set(4, cap_height)


time.sleep(1.0)
#_, black_frame = cap.read()

frame_width = 1024
frame_height = 768

resize_width_factor = frame_width / cap_width
resize_heigth_factor = frame_height / cap_height

black_frame = np.zeros((frame_height, frame_width, 3), np.uint8)
print(frame_width)
print(frame_height)

cv2.rectangle(black_frame, (0, 0), (frame_width, frame_height), (0, 0, 0), -1)

painter = Painter(black_frame).start()

if enable_fps_timer == True:
    timer2 = time.time()



reset_area_width = 50
reset_area_height = 50

save_area_width = 50
save_area_height = 50
save_area_y = frame_height - 50

def reset_canvas():
    cv2.rectangle(black_frame, (0, 0), (frame_width, frame_height), (0, 0, 0), -1)
    cv2.rectangle(black_frame, (0, 0), (reset_area_width, reset_area_height), (10, 10, 10), -1)
    cv2.rectangle(black_frame, (0, save_area_y), (save_area_width, save_area_y + save_area_height), (20, 20, 20), -1)

reset_canvas()

counter = 0

while True:


    if enable_fps_timer == True:
        timer1 = time.time()

    _, frame = cap.read()
    frame = cv2.flip(frame, 1)

    painter.frame = frame

    brush_x = int(painter.brush_x * resize_width_factor)
    brush_y = int(painter.brush_y * resize_heigth_factor)
    brush_radius = int(painter.brush_radius * resize_width_factor)

    cv2.circle(black_frame, (brush_x, brush_y), brush_radius, (255, 255, 255), -1)

    if brush_x < reset_area_width and brush_y < reset_area_height:
        reset_canvas()
        time.sleep(1)

    if brush_x < save_area_width and brush_y > save_area_y:
        counter += 1
        localPath = 'images/image1000'+str(counter)+'.jpg'
        cv2.imwrite(localPath,black_frame)
        time.sleep(1)


    if enable_fps_timer == True:
        print("FPS: " + str(1/((timer1-timer2))))
        timer2 = time.time()

    cv2.imshow("Frame", black_frame)
    key = cv2.waitKey(1)
    
    if key == 27:
        break
    
cap.release()
cv2.destroyAllWindows()

