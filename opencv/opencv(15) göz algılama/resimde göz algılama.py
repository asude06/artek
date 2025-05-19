import cv2
# önce resimdeki yüzü bulucaz sonra o bölgedeki gözleri bulup çerçeveliycez

img = cv2.imread("C:\\Users\\Asus\\Desktop\\artek\\face.png")

face_cascade = cv2.CascadeClassifier("C:\\Users\\Asus\\Desktop\\artek\\4.1 frontalface.xml.xml")
eye_cascade = cv2.CascadeClassifier("C:\\Users\\Asus\\Desktop\\artek\\5.1 eye.xml.xml")

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray,1.3,5)

for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)

# yüzün old p,kselleri bu değişkenlere atadık
img2 = img[y:y+h,x:x+w]
gray2 = gray[y:y+h,x:x+w]

eyes = eye_cascade.detectMultiScale(gray2) # gözleri buldurucaz

for (ex,ey,ew,eh) in eyes:
    cv2.rectangle(img2,(ex,ey),(ex+ew,ey+eh),(255,0,0),2)

cv2.imshow("img",img)
cv2.waitKey(0)
cv2.destroyAllWindows()