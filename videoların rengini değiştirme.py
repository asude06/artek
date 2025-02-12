# videonun rengini direkt değiştiremiyoruz tek tek framlerinin rengini değiştirerek yapıyoruz

import cv2
import numpy as np

cap = cv2.VideoCapture("C:\\Users\\Asus\\Desktop\\artek\\cicekli.mp4")

while True:
    ret, frame = cap.read()

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if ret == 0:
        break

    cv2.imshow("video",frame)

    if cv2.waitKey(10) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()