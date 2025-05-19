import cv2

img = cv2.imread("C:\\Users\\Asus\\Desktop\\artek\\face.png")
face_cascade = cv2.CascadeClassifier('C:\\Users\\Asus\\Desktop\\artek\\4.1 frontalface.xml.xml') # hazır kullandığımız bir dosya bu
#Haar-like özellikleri kolay algılayabilmek için resmimizi boz(gri) tonlara çevirelim.
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray,1.3,7) # yüzlerin koordinatlarını veriyor, hangi ölçekte küçültüceği, kaç pencerer sonrası yüz old söyleyeceği/ koordinatları faces değişkenin içine tuple olarak saklayacak

for(x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2) # sol üst ve sağ alt noktalarını yazıyoruz

cv2.imshow("img",img)

cv2.waitKey(0)
cv2.destroyAllWindows()