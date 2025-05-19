import cv2

vid = cv2.VideoCapture('C:\\Users\\Asus\\Desktop\\artek\\8.1 smile.mp4.mp4') # buraya 0 yazarsak webcamde açılır ve ordaki gülümsememizi algılar

face_cascade = cv2.CascadeClassifier("C:\\Users\\Asus\\Desktop\\artek\\4.1 frontalface.xml.xml")
smile_cascade = cv2.CascadeClassifier("C:\\Users\\Asus\\Desktop\\artek\\4.2 smile.xml.xml")

while True:
    ret,frame = vid.read()
    frame = cv2.resize(frame,(640,480))
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray,1.3,5)
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)

    roi_frame = frame[y:y+h,x:x+w]
    roi_gray = gray[y:y+h,x:x+w]

    smiles = smile_cascade.detectMultiScale(roi_gray,1.2,2)
    for (sx,sy,sw,sh) in smiles:
        cv2.rectangle(roi_frame,(sx,sy),(sx+sw,sy+sh),(0,255,0),2)

    cv2.imshow('video',frame)

    if cv2.waitKey(20) & 0xFF == ord("q"):
        break
vid.release()
cv2.destroyAllWindows()