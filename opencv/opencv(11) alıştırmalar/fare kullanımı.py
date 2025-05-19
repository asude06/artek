# pencerede üstüne tıkladığımız yerlerde çemberler oluşmasını istiyoruz

import cv2

cap = cv2.VideoCapture("C:\\Users\\Asus\\Desktop\\artek\\line.mp4")

circles = []

def mouse(event,x,y,flags,params):
    if event == cv2.EVENT_LBUTTONDOWN: # farede sol tuşa bastığımı anlar
        circles.append((x,y)) # dokunduğum noktayı listeye ekle

cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame",mouse) # yaptığımız işlemi anlayacak fonksiyon, frame üzerine şu işlemleri yapıyorum

while 1:
    _,frame = cap.read()
    frame = cv2.resize(frame,(640,480))

    for center in circles:
        cv2.circle(frame,center,20,(255,0,0),-1)

    cv2.imshow("Frame",frame)
    key = cv2.waitKey(1)
    if key == 27: # esc tuşu demek
        break
    elif key == ord("h"): # h ye bastığımızda ekranı temizliyor
        circles = []

cap.release()
cv2.destroyAllWindows()
