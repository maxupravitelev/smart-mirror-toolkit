import cv2

background_image=None

cap=cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray_frame=cv2.GaussianBlur(gray_frame,(25,25),0)

    if background_image is None:
        background_image=gray_frame
        continue

    delta=cv2.absdiff(background_image,gray_frame)
    threshold=cv2.threshold(delta, 30, 255, cv2.THRESH_BINARY)[1]
    (contours,_)=cv2.findContours(threshold,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        (x, y, w, h)=cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255,255,255), 10)
    
    #cv2.imshow("Color Frame",frame)
    cv2.namedWindow('Video feed', cv2.WINDOW_FREERATIO)
    cv2.setWindowProperty('Video feed', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('Video feed', cv2.flip(frame, 1))

    #cv2.imshow("gray_frame Frame",gray_frame)
    #cv2.imshow("Delta Frame",delta)
    #cv2.imshow("Threshold Frame",threshold)
    

    key=cv2.waitKey(1)

    if key==ord('x'):
        break

cap.release()
cv2.destroyAllWindows

# Built upon:
# https://github.com/arindomjit/Motion_Detected_Alarm/blob/master/motion_detector.py