import cv2
import numpy as np
import time

gpio_motor = False
if gpio_motor == True:
    from modules.gpio_motor import GPIO_motor
    motor = GPIO_motor()

camera_mode = "webcam"

# init videostream (separate thread)
if camera_mode == "webcam":

    # # start raspivid in a subprocess
    # import subprocess
    # cmd = "raspivid -n -t 0 -n  -w 1024 -h 768  -ih -fl -l -o - | /bin/nc -lvp 5000"
    # subprocess.Popen(cmd, shell=True)
    from modules.cam import VideoStream
    time.sleep(2)
    cap = VideoStream(src=0).start()
else: 
    from modules.PiCam import PiCam 
    cap = PiCam().start()

time.sleep(0.5)
frame = cap.read()
frame_height = frame.shape[0]
frame_width = frame.shape[1]

x_medium = int(frame_width / 2)

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
            #last_x_medium = x_medium
            #x_medium = int((x + x + w) / 2)

            # if x < x_medium:
            #     print("left")
            #     motor.move_non_threaded(1, "left")
            #     #time.sleep(0.1)
            # elif x == x_medium:
            #     print("stay")
            # else:
            #     print("right")
            #     motor.move_non_threaded(1, "right")
            #     #time.sleep(0.1)


            break
        
    return frame

while True:
    frame = cap.read()
    
    frame = cv2.flip(frame, 1)

    frame = trackcolor(frame)


    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    
    if key == 27:
        break
    
cap.release()
cv2.destroyAllWindows()

# Built upon: https://pysource.com/2019/06/05/control-webcam-with-servo-motor-and-raspberry-pi-opencv-with-python/