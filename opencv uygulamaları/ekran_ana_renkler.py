import cv2
import numpy as np

OUTPUT_PATH = "output.avi"
FPS = 20
CODEC = "MJPG"

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Kamera açılamadı")
    exit()

ret, frame = cap.read()
h, w = frame.shape[:2]

fourcc = cv2.VideoWriter_fourcc(*CODEC)
writer = cv2.VideoWriter(OUTPUT_PATH, fourcc, FPS, (w*2, h*2))

zeros = np.zeros((h, w), dtype="uint8")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (w, h))
    frame = cv2.flip(frame, 1) #yansımasını aldık

    B, G, R = cv2.split(frame)

    # tek kanallı goruntuler olusturuyruz
    R_frame = cv2.merge([zeros, zeros, R])
    G_frame = cv2.merge([zeros, G, zeros])
    B_frame = cv2.merge([B, zeros, zeros])

    output = np.zeros((h*2, w*2, 3), dtype="uint8") #4lü tablo seklinde
    output[0:h, 0:w] = frame
    output[0:h, w:w*2] = R_frame
    output[h:h*2, w:w*2] = G_frame
    output[h:h*2, 0:w] = B_frame

    writer.write(output)

    cv2.imshow("Frame", frame)

    display = cv2.resize(output, None, fx=0.6, fy=0.6) #yeniden boyutlandırma yaptık
    cv2.imshow("Output", display)


    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
writer.release()
cv2.destroyAllWindows()