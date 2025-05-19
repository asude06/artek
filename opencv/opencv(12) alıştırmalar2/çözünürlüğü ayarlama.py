#yatay ve dikeydeki piksel sayısını değiştiriyoruz çözünürlük değiştirirken
import cv2

windowName = "Live Video"
cv2.namedWindow(windowName) #pencere oluşturduk

cap = cv2.VideoCapture(0) # webcam den görüntü alıyoruz

print("Width: "+str(cap.get(3))) # görüntünün enini verir / yatay
print("Height: "+str(cap.get(4))) #görüntünün yüksekliğini verir / dikey

cap.set(3,1280) # değişiklik yapıyoruz
cap.set(4,720)

print("Width*: "+str(cap.get(3)))
print("Height*: "+str(cap.get(4)))

while True:
    _,frame = cap.read()

    frame = cv2.flip(frame,1) #y eksenine göre simetriği

    cv2.imshow(windowName,frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()