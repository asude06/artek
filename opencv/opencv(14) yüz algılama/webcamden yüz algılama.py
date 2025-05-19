import cv2

from artek.görevler.gorev import frame

vid = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier("C:\\Users\\Asus\\Desktop\\artek\\4.1 frontalface.xml.xml")

while True:
    _,frame = vid.read()
    frame = cv2.flip(frame,1)

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray,1.6,5) #en az 5 tane yüz bulsun ki çizimi yapsın

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

    cv2.imshow("img",frame)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()