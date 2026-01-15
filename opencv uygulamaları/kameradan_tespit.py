import cv2
import time
import datetime
import imutils
from collections import deque

cap = cv2.VideoCapture(0)
time.sleep(2)

BUFFER_SIZE = 32
buffer = deque(maxlen=BUFFER_SIZE) #32 frame i tutabilmek icin kuyruk kullandık

recording = False
writer = None
after_event_frames = 0

greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = imutils.resize(frame, width=600)
    frame = cv2.flip(frame, 1)

    buffer.append(frame.copy()) # eger 32 den fazlaysa otomatik siler

    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2) #gercek sınırları korur
    mask = cv2.dilate(mask, None, iterations=2) #boslukları doldurur

    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    event = False

    if cnts:
        c = max(cnts, key=cv2.contourArea) #en buyuk yesil nesne secciliyor
        ((x, y), radius) = cv2.minEnclosingCircle(c) # nesneyi daire olarak kabul ediyoruz

        if radius > 10: #yarıcapi
            event = True
            after_event_frames = 0
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 0, 255), 2) #kırmızı ile cerveler

            if not recording:
                ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
                writer = cv2.VideoWriter( #videoyu olusturmaya baslar
                    f"{ts}.avi",
                    cv2.VideoWriter_fourcc(*"MJPG"),
                    20,
                    (frame.shape[1], frame.shape[0])
                )

                for f in buffer:  # olay öncesi frameler
                    writer.write(f)

                recording = True

    if recording:
        writer.write(frame)

        if not event:
            after_event_frames += 1

        if after_event_frames >= BUFFER_SIZE:
            writer.release()
            recording = False

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

if recording:
    writer.release()

cap.release()
cv2.destroyAllWindows()