import cv2
import numpy as np
import time

from modules.painter import Painter



camera_mode = "picam"

# init videostream (separate thread)
if camera_mode == "webcam":

    # start raspivid in a subprocess
    import subprocess
    cmd = "raspivid -n -t 0 -n  -w 1024 -h 768  -ih -fl -l -o - | /bin/nc -lvp 5000"
    subprocess.Popen(cmd, shell=True)
    from modules.cam import VideoStream
    time.sleep(2)
    cap = VideoStream(src=0).start()
else: 
    from modules.PiCam import PiCam 
    cap = PiCam().start()


# cap = cv2.VideoCapture(0)
# # Set camera resolution
# cap.set(3, 1024)
# cap.set(4, 768)

time.sleep(1.0)
black_frame = cap.read()
# cv2.rectangle(black_frame, (0, 0), (1, 1), (255, 0, 0), 2)

frame_width = int(black_frame.shape[1]) 
frame_height = int(black_frame.shape[0])
print(frame_width)
print(frame_height)

cv2.rectangle(black_frame, (0, 0), (frame_width, frame_height), (0, 0, 0), -1)

painter = Painter(black_frame).start()

while True:
    frame = cap.read()
    frame = cv2.flip(frame, 1)

    painter.frame = frame
    
    cv2.circle(black_frame, (painter.brush_x, painter.brush_y), 5, (255, 255, 255), 5)

    cv2.imshow("Frame", black_frame)
    key = cv2.waitKey(1)
    
    if key == 27:
        break
    
cap.release()
cv2.destroyAllWindows()

