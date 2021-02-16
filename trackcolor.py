import cv2
import numpy as np
import time


gpio_motor = True

if gpio_motor == True:
    from modules.gpio_motor import GPIO_motor
    motor = GPIO_motor()



cap = cv2.VideoCapture(0)
# Set camera resolution
cap.set(3, 480)
cap.set(4, 320)
_, frame = cap.read()
rows, cols, _ = frame.shape

x_medium = int(cols / 2)

last_x_medium = int(cols / 2)

while True:
    _, frame = cap.read()
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
        if cv2.contourArea(cnt) > 1000:
            (x, y, w, h) = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            last_x_medium = x_medium
            x_medium = int((x + x + w) / 2)

            if last_x_medium > x_medium:
                print("left")
                motor.move_non_threaded(1, "left")
                #time.sleep(0.1)
            elif last_x_medium == x_medium:
                print("stay")
            else:
                print("right")
                motor.move_non_threaded(1, "right")
                #time.sleep(0.1)


            break


    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    
    if key == 27:
        break
    
cap.release()
cv2.destroyAllWindows()

# Built upon: https://pysource.com/2019/06/05/control-webcam-with-servo-motor-and-raspberry-pi-opencv-with-python/