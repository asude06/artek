# insan bedenini algılayamıyor çünkü çok farklılıklar var kestiremiyor
import cv2

img = cv2.imread("C:\\Users\\Asus\\Desktop\\artek\\body.jpg")

body_cascade = cv2.CascadeClassifier('C:\\Users\\Asus\\Desktop\\artek\\fullbody.xml.xml')

gray =cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

bodies = body_cascade.detectMultiScale(gray,1.8,2)

for (x,y,w,h) in bodies:
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)

cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()