import cv2
import numpy as np

img = cv2.imread("C:\\Users\\Asus\\Desktop\\artek\\para.jpeg")

img = cv2.resize(img,(640,480))

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_blur = cv2.medianBlur(gray,9)

circles = cv2.HoughCircles(img_blur,cv2.HOUGH_GRADIENT,1,img.shape[0]/5.5,param1=300,param2=20,minRadius=40,maxRadius=330) # bu degerleri degistirdm
# print(circles) # çemberlerin konumunun veren bir liste

if circles is not None:
    circles = np.uint16(np.around(circles))
    adet = len(circles[0]) # listenin uzunluğuna göre kaç adet old buluyor, ve bu sabit 0 dan başka bi şey yazılmıyor

    for i in circles[0,:]:
        cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)

cv2.putText(img,'bulunan para sayisi: '+ f'{adet}',(90,50),2,1,(0,0,255),2,5,0)

cv2.imshow('img',img)
print(f"görselde {adet} adet çember var")

cv2.waitKey(0)
cv2.destroyAllWindows()