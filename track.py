import cv2
import numpy as np
# from PCA9685 import PCA9685

# pwm = PCA9685(0x40, debug=False)
# pwm.setPWMFreq(50)
# pwm.setServoPosition(0, 90)

cap = cv2.VideoCapture(0)
# Set camera resolution
cap.set(3, 480)
cap.set(4, 320)
_, frame = cap.read()
rows, cols, _ = frame.shape

x_medium = int(cols / 2)
center = int(cols / 2)
position = 90 # degrees

while True:
    _, frame = cap.read()
    #hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # red color
    # low_red = np.array([161, 155, 84])
    # high_red = np.array([179, 255, 255])

    low_red = np.array([0, 0, 0])
    high_red = np.array([20, 20, 20])

    red_mask = cv2.inRange(frame, low_red, high_red)
    # print(red_mask)
    contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)

    for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            
            x_medium = int((x + x + w) / 2)
            print(x_medium)
            break
        
    cv2.line(frame, (x_medium, 0), (x_medium, 480), (0, 255, 0), 2)

    # Move servo motor
    # if x_medium < center -30:
    #     position += 1
    # elif x_medium > center + 30:
    #     position -= 1
    # pwm.setServoPosition(0, position)

    #cv2.line(frame, (x_medium, 0), (x_medium, 480), (0, 255, 0), 2)
    
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    
    if key == 27:
        break
    
cap.release()
cv2.destroyAllWindows()

# Built upon: https://pysource.com/2019/06/05/control-webcam-with-servo-motor-and-raspberry-pi-opencv-with-python/