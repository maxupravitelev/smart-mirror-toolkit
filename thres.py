import cv2
cap = cv2.VideoCapture(0)

# windowName = "Live"
# cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
# cv2.setWindowProperty(windowName,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

while True:
    ret, img = cap.read()
    
    cv2.namedWindow('Video feed', cv2.WINDOW_FREERATIO)
    cv2.setWindowProperty('Video feed', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 10, 70)
    ret, mask = cv2.threshold(canny, 70, 255, cv2.THRESH_BINARY)
    cv2.imshow('Video feed', cv2.flip(mask, 1))
#    cv2.imshow('Video feed', mask)
    
    if cv2.waitKey(1) == 13:
        break
        
cap.release()
cv2.destroyAllWindows()
