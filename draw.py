import cv2
import numpy as np


cap = cv2.VideoCapture(0)
# Set camera resolution
cap.set(3, 480)
cap.set(4, 320)


_, black_frame = cap.read()

frame_width = int(cap.get(3)) 
frame_height = int(cap.get(4))
print(frame_width)
print(frame_height)

cv2.rectangle(black_frame, (0, 0), (frame_width, frame_height), (0, 0, 0), -1)


while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # red color
    low_red = np.array([161, 155, 84])
    high_red = np.array([179, 255, 255])

#     low_red = np.array([0, 0, 0])
#     high_red = np.array([20, 20, 20])

    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    # print(red_mask)
    contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)

    for cnt in contours:
        # if cv2.contourArea(cnt) > 1000:
            (x, y, w, h) = cv2.boundingRect(cnt)
            radius = int(w / 10)
            cv2.circle(black_frame, (x, y), radius, (255, 255, 255), -1)


            break


    cv2.imshow("Frame", black_frame)
    key = cv2.waitKey(1)
    
    if key == 27:
        break
    
cap.release()
cv2.destroyAllWindows()

# Built upon: https://pysource.com/2019/06/05/control-webcam-with-servo-motor-and-raspberry-pi-opencv-with-python/
