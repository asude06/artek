import imutils
import cv2
import numpy as np

camera = cv2.VideoCapture(0)

while True:
    grabbed, frame = camera.read()
    frame = cv2.flip(frame, 1) #yansımasını aldık
    status = "No Targets"

    if not grabbed:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    edged = cv2.Canny(blurred, 50, 150)

    cnts = cv2.findContours(edged.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        area = cv2.contourArea(c)
        if area < 300:
            continue

        peri = cv2.arcLength(c, True) #konturun cevre uzunlugunu hesaplıyor 0 ise işlemz
        if peri == 0:
            continue

        circularity = 4 * np.pi * area / (peri * peri) #tam bi daire olması için 1 olmalı

        (x, y, w, h) = cv2.boundingRect(c) #konturu dortgen icine alıyor
        aspectRatio = w / float(h)

        if circularity > 0.75 and 0.8 <= aspectRatio <= 1.2:
            cv2.drawContours(frame, [c], -1, (0, 0, 255), 3) # kontur kenarları kırmızı oluoyr
            status = "Circular Target"

            # Merkez işareti
            M = cv2.moments(c)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                cv2.line(frame, (cX - 15, cY),
                         (cX + 15, cY), (0, 0, 255), 2)
                cv2.line(frame, (cX, cY - 15),
                         (cX, cY + 15), (0, 0, 255), 2)

    cv2.putText(frame, status, (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                (0, 0, 255), 2)

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()