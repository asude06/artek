import cv2

vid = cv2.VideoCapture('C:\\Users\\Asus\\Desktop\\artek\\6.2 car.mp4.mp4')

car_cascade = cv2.CascadeClassifier('C:\\Users\\Asus\\Desktop\\artek\\2.3 car.xml.xml')

while True:
    ret, frame = vid.read()
    frame = cv2.resize(frame,(640,360))

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    cars = car_cascade.detectMultiScale(gray,1.2,2)

    for (x,y,w,h) in cars:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)
    cv2.imshow('video',frame)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()
