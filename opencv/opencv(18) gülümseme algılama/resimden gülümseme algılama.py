import cv2

img = cv2.imread('C:\\Users\\Asus\\Desktop\\artek\\smile.jpg.jpg')

face_cascade = cv2.CascadeClassifier("C:\\Users\\Asus\\Desktop\\artek\\4.1 frontalface.xml.xml")
smile_cascade = cv2.CascadeClassifier("C:\\Users\\Asus\\Desktop\\artek\\4.2 smile.xml.xml")

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray,1.3,5)

for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)

# sadece yüz üzerinde arama yapmak için kordinatları sabitledik, yüz bölgesi hapsedilerek yüksek başarım elde etmek
    roi_img = img[y:y+h,x:x+h]
    roi_gray = gray[y:y+h,x:x+h]

    smiles = smile_cascade.detectMultiScale(roi_gray,1.3,5)

    for (sx,sy,sw,sh) in smiles:
        cv2.rectangle(roi_img,(sx,sy),(sx+sw,sy+sh),(0,255,0),2)

    cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()