import cv2
import numpy as np

cap = cv2.VideoCapture("C:\\Users\\Asus\\Desktop\\artek\\dog.mp4")

while True:
    ret,frame = cap.read()

    if ret == 0:
        break

    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) #nesnenin takibi için hsv ye çevirmek gerekiyor

    sensitivity = 15
    lower_white = np.array([0,0,255-sensitivity])
    upper_white = np.array([255,sensitivity,255])

    mask = cv2.inRange(hsv,lower_white,upper_white)
    res = cv2.bitwise_and(frame,frame,mask=mask) # bi videonun old frame bi de kazıdığı frame

    cv2.imshow("frame",frame)
    #cv2.imshow("mask",mask)
    cv2.imshow("result",res)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()