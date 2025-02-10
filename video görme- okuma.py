import cv2


# vidoelar arka arkaya hızlıca gösterilen karelerden oluşur
# cap kare demek galiba

# webcam den bakacağımızda
"""
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame,1) # framein y eksenine göre tersi oluyor ki aynadaki gibi görünsün

    cv2.imshow("webcam",frame)

    if cv2.waitKey(1) & 0xFF == ord("q"): # ifade q nun makine dilindeki karşılığı
        break

cap.release()
cv2.destroyAllWindows()
"""

# hazır bir videoyu açarken

cap = cv2.VideoCapture("videom.mp4")

while True:
    ret, frame = cap.read()
    if ret == 0: # video bittiğinde kapansın demek, retin okuyacağı başka bir kare kalmadığında
        break

    frame = cv2.flip(frame,1) # framein y eksenine göre tersi oluyor ki aynadaki gibi görünsün

    cv2.imshow("videom",frame)

    if cv2.waitKey(20) & 0xFF == ord("q"): # ifade q nun makine dilindeki karşılığı
        break

cap.release()
cv2.destroyAllWindows()

