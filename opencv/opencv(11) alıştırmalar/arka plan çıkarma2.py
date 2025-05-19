import cv2
import numpy as np
from numpy.ma.core import subtract

cap = cv2.VideoCapture("C:\\Users\\Asus\\Desktop\\artek\\car.mp4")
subtractor = cv2.createBackgroundSubtractorMOG2(history=100,varThreshold=50,detectShadows=True) # her bir frame değişiklik olabilir mesela gölge gibi
# diğer manuele göre daha daha net görüntü oluşturuyor siyah beyaz farkı belirgin

while True:
    _,frame = cap.read()
    frame = cv2.resize(frame,(640,480))
    mask = subtractor.apply(frame)

    cv2.imshow("frame",frame)
    cv2.imshow("mask",mask)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()