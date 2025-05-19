#ilk resimden diğer resime geçiş yapacak
#kızakta kaydırma yaparken calı olarak değer değişiyor ağırlık oranları
import cv2

def nothing(x): #trackbar için
    pass

img1 = cv2.imread("aircraft.jpg")
img1 = cv2.resize(img1,(640,480))

img2 = cv2.imread("balls.jpg")
img2 = cv2.resize(img2,(640,480))

output = cv2.addWeighted(img1,0.5,img2,0.5,0) #(oranların toplamı 1 olmalı/varsayılan olarak yazdık onları aşağıda değiştiriyoruz)ağırlıklarını değiştirecez birinin yoğunluğunu arttırıp diğerininkini azaltıcaz
windowName = "Transition Program"
cv2.namedWindow(windowName)

cv2.createTrackbar("Alpha-Beta",windowName,0,1000,nothing)

while True: # değişiklik görmek istediğimiz için bir while döngüsü oluşturucaz
    cv2.imshow(windowName,output)
    alpha = cv2.getTrackbarPos("Alpha-Beta",windowName)/1000
    beta = 1-alpha
    output = cv2.addWeighted(img1,alpha,img2,beta,0)
    print(alpha,beta)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
