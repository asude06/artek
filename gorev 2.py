import cv2
import numpy as np

cap = cv2.VideoCapture("C:\\Users\\Asus\\Desktop\\kaplumbağa.mp4")

while True:

    ret,frame = cap.read()

    if ret == 0:
        break

    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    lower_greenish_brown = np.array([0,0,0])
    upper_greenish_brown = np.array([88,255,200])

    mask = cv2.inRange(hsv,lower_greenish_brown,upper_greenish_brown)

    result = cv2.bitwise_and(frame,frame,mask=mask)

    cv2.imshow("frame",frame)
    cv2.imshow("result",result)

    if cv2.waitKey(10) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()