# hiçbir şey bulamadı işe yaramadı cascadein kötü özelliği
import cv2

img = cv2.imread('C:\\Users\\Asus\\Desktop\\artek\\2.2 car.jpg.jpg')

car_cascade = cv2.CascadeClassifier('C:\\Users\\Asus\\Desktop\\artek\\2.3 car.xml.xml')

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cars = car_cascade.detectMultiScale(gray,1.1,1) # burdaki değerleri değiştirebiliriz 1.4,2 idi// şu an yeni değerlerle 4 tanesini bulabildi

for (x,y,w,h) in cars:
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)

cv2.imshow('image',img)

cv2.waitKey(0)
cv2.destroyAllWindows()
