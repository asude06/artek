import cv2
import numpy as np
import math

def findMaxContour(contours):
    max_i = 0
    max_area = 0
    for i in range(len(contours)):  # max alanı bulmak için alanları karşılaştıracak
        area_face = cv2.contourArea(contours[i])

        if max_area<area_face:
            max_area = area_face
            max_i = i
        try:
            c = contours[max_i] # eğer burda bulamazsa aşağıda onu sıfır olarak atıyacak
        except:
            contours = [0] # boş dizi eğer yukarda alan bulamazsa
            c = contours[0]
        return c

cap = cv2.VideoCapture(0) # webcamden görüntü alıyoruz

while True:
    ret,frame = cap.read()
    frame = cv2.flip(frame,1) #y eksenine göre takla attırıyoruz

    roi = frame[50:350,100:400] #frame[y1:y2,x1:x2]
    cv2.rectangle(frame,(100,50),(400,350),(0,0,255),0) #ekran üzerinde bir dörtgen oluşturacak kalınığı 0 olmalı yoksa mask işlemine girer

    hsv = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)

    lower_color = np.array([0,20,50],dtype=np.uint8)
    upper_color = np.array([30,100,255],dtype = np.uint8)

    mask = cv2.inRange(hsv,lower_color,upper_color)

    kernel = np.ones((3,3),np.uint8)
    mask = cv2.dilate(mask,kernel,iterations=1)
    mask = cv2.medianBlur(mask,15)

    contours,_ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        try:
            c = findMaxContour(contours)

            extLeft = tuple(c[c[:,:,0].argmin()][0]) # tüm konturları dolaşıp en küçük x i bulacak
            extRight = tuple(c[c[:, :, 0].argmax()][0]) # x in en büyük olduğu değeri bulur
            extTop = tuple(c[c[:, :, 1].argmin()][0]) # y nin en küçük olduğu değeri bulur
            extBot = tuple(c[c[:, :, 1].argmax()][0]) # y nin en büyük olduğunu bulur

            cv2.circle(roi, extLeft, 5, (0, 255, 0), 2)  # uç noktalara çemberler çizdik
            cv2.circle(roi, extRight, 5, (0, 255, 0), 2)
            cv2.circle(roi, extTop, 5, (0, 255, 0), 2)
            cv2.circle(roi,extBot,5,(0,255,0),2)

            cv2.line(roi,extLeft,extTop,(255,0,0),2) #çemberleri birleştirip şekil oluşturucaz
            cv2.line(roi, extRight, extTop, (255, 0, 0), 2)
            cv2.line(roi, extRight, extBot, (255, 0, 0), 2)
            cv2.line(roi, extLeft, extBot, (255, 0, 0), 2)

            a = math.sqrt((extRight[0] - extTop[0]) ** 2 + (extRight[1] - extTop[1]) ** 2)  #[0] x e, [1] y ye karşılık geliyor eksenlerden çıkarma işlemi yapıp pisagorla kenar uzunluğunu buluyoruz
            b = math.sqrt((extBot[0] - extRight[0]) ** 2 + (extBot[1] - extRight[1]) ** 2)
            c = math.sqrt((extBot[0] - extTop[0]) ** 2 + (extBot[1] - extTop[1]) ** 2)

            try:
                angle_ab = int(math.acos((a**2+b**2-c**2)/(2*b*c)) * 57) # 2 kenar arası açıyı kosinüs teoreminden bulduk
                cv2.putText(roi,str(angle_ab),(extRight[0] - 100+50,extRight[1]),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv2.LINE_AA) #açı değerini şeklin içindeki yerine yazdık, 0 olma ihtimaline karşı try kullandık
            except:
                cv2.putText(roi, " ? ", (extRight[0] - 100+50, extRight[1]), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2,cv2.LINE_AA)
        except:
            pass

    cv2.imshow("frame",frame)
    cv2.imshow("roi", roi)
    cv2.imshow("mask", mask)

    if cv2.waitKey(10) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()