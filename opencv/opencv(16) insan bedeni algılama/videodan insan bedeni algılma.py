#vücut algılamada işe yaramıyor kötü tespit edemiyor hatalar verip duruyor
import cv2

vid = cv2.VideoCapture('C:\\Users\\Asus\\Desktop\\artek\\body.mp4')

body_cascade = cv2.CascadeClassifier('C:\\Users\\Asus\\Desktop\\artek\\fullbody.xml.xml')

while True:
    ret,frame = vid.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    bodies = body_cascade.detectMultiScale(gray,1.1,4)

    for (x,y,w,h) in bodies:
        cv2.rectangle(frame,(x,y),(y+h,x+w),(0,0,255),3)
    cv2.imshow("video",frame)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()