import cv2
import numpy as np

cap = cv2.VideoCapture("C:\\Users\\Asus\\Desktop\\artek\\kaplumbağa.mp4")

while True:
    ret,frame = cap.read()

    if ret == 0:
        break

    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    lower_brown_greenish = np.array([0, 0, 0])
    upper_brown_greenish = np.array([88, 255, 255])

    mask = cv2.inRange(hsv,lower_brown_greenish,upper_brown_greenish)
    res = cv2.bitwise_and(frame,frame,mask=mask)

    cv2.imshow("frame",frame)

    cv2.imshow("result",res)

    if cv2.waitKey(10) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()