# gözü roi alanı yapıcaz beyaz ve irisi masklıycaz, göz bebeğinin old yerer şekil koyucaz ve şeklin hareketine göre çıkarım yapıcaz

import cv2

vid = cv2.VideoCapture("C:\\Users\\Asus\\Desktop\\artek\\eye.mp4")

while True:
    ret,frame = vid.read() #ret framelerin doğru çekilip çekilmediğine bakıyor

    if ret is False:
        break

    roi = frame[80:210, 230:450]
    rows,cols,_ = roi.shape # kullanmadığımız değerler için _ koyuyoruz
    gray = cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
    _,threshold = cv2.threshold(gray,3,255,cv2.THRESH_BINARY_INV)

    contours,_ = cv2.findContours(threshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = lambda x: cv2.contourArea(x), reverse=True) # konturları sırala lambda fonk a göre büyükten küçüğe gibi

    for cnt in contours:
        (x,y,w,h) = cv2.boundingRect(cnt) # dörtgenin 2 noktası var sol üst ve sağ alt, w genişlik, h yükseklik ; sol üstteki noktanın kpprdinatlarını (0,0) olarak alıyoruz
        cv2.rectangle(roi,(x,y),(x+w,y+h),(255,0,0),2)
        cv2.line(roi,(x+int(w/2),0),(x+int(w/2),rows),(0,255,0),2)
        cv2.line(roi, (0,y+int(h/2)),(cols,y+int(h/2)), (0, 255, 0), 2)
        break

    frame[80:210, 230:450] = roi # roi için yaptığımız tüm işlemleri soldaki koordinatlara uyguluyoruz bu şekilde işlem görüntünün üstüne taşınmış oluyor

    cv2.imshow("frame",frame)

    if cv2.waitKey(80) & 0xFF == ord("q"):
        break

vid.release()
cv2.destroyAllWindows()