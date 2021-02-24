import cv2
import time
import argparse

## parse args from command line
parser = argparse.ArgumentParser()
parser.add_argument("--mode", type=str, default="threshold",
        help="choose effects mode") 
args = vars(parser.parse_args())
mode = args["mode"]

cap = cv2.VideoCapture(0)
time.sleep(1)

def show_threshold(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)
    canny = cv2.Canny(blurred_frame, 10, 70)
    _, threshold_frame = cv2.threshold(canny, 70, 255, cv2.THRESH_BINARY)

    return threshold_frame


while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    
    # cv2.namedWindow('frame', cv2.WINDOW_FREERATIO)
    # cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    if mode == "threshold":
        frame = show_threshold(frame)

    cv2.imshow('frame', frame)
    
    if cv2.waitKey(1) == 27:
        break
        
cap.release()
cv2.destroyAllWindows()
