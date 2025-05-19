import cv2
import numpy as np
import pytesseract
import imutils

img = cv2.imread("C:\\Users\\Asus\\Desktop\\artek\\9.1 licence_plate.jpg.jpg")
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
filtered = cv2.bilateralFilter(gray, 6, 250,250) #yumuşatma işlemi yapıyoruz
edged = cv2.Canny(filtered,30,200) #kenarları belirliyoruz, köşeleri bulduk


contours = cv2.findContours(edged,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #sınırları çiziyoruz koordinat bulmaya yarıyor da diyebiliriz
cnts = imutils.grab_contours(contours) #uygun contoursları yakala
cnts = sorted(cnts,key=cv2.contourArea,reverse=True)[:10] # koordinatların dikdörtgen oluşturduğunu yakala, kapalı alan buldun mu
screen = None

for c in cnts:
    epsilon = 0.018*cv2.arcLength(c,True) #konturlar yaylarının uzunluklarını buluyor
    approx = cv2.approxPolyDP(c,epsilon,True) #dikdörtgen şekil biraz daha yamuksa onu telafi etsin diye yaklaşımlar yapıyor
    if len(approx) == 4: #4 köşeliyse dikdörtgendir
        screen = approx #screen ı buna eşitle dörtgen old belirt gibi, koordinatları tutuyor
        break

mask = np.zeros(gray.shape,np.uint8) #resim tamamen siya oldu şu an
new_img = cv2.drawContours(mask,[screen],0,(255,255,255),-1) #plaka hariç her yer siyah olacak, plaka kısmı beyaz olacak
new_img = cv2.bitwise_and(img,img,mask = mask) # plaka kısmındaki beyazlığa plakayı yapıştırıyor

(x,y) = np.where(mask== 255) #beyaz yerlerin koordinatlarını tutuyor

(topx,topy) = (np.min(x),np.min(y))
(bottomx,bottomy) = (np.max(x),np.max(y))

cropped = gray[topx:bottomx+1,topy:bottomy+1] #kırptı

text = pytesseract.image_to_string(cropped,lang="eng")
print("detected text",text)

cv2.imshow("original",img)
# cv2.imshow("gray",gray)
# cv2.imshow("filtered",filtered)
# cv2.imshow("edged",edged)

cv2.waitKey(0)
cv2.destroyAllWindows()