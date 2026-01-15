import cv2
import imutils

IMAGE_PATH = "barkod.webp"   

image = cv2.imread(IMAGE_PATH)
if image is None:
    raise FileNotFoundError("Resim bulunamadı!")

# griye çevir
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Scharr gradientleri
ddepth = cv2.CV_32F
gradX = cv2.Sobel(gray, ddepth=ddepth, dx=1, dy=0, ksize=-1) #güçlü , yogunluk degisimini olcer kenarlar icin, dikey cizgiler
gradY = cv2.Sobel(gray, ddepth=ddepth, dx=0, dy=1, ksize=-1) #zayif , yatay cizgiler

# x - y gradient
gradient = cv2.subtract(gradX, gradY) #yuksek x, dusuk y, barkod bolgesi parlak
gradient = cv2.convertScaleAbs(gradient)

# blur + threshold
blurred = cv2.blur(gradient, (9, 9))
_, thresh = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY) # 225 ten buyukse beyaz

# morfolojik kapama bosluklardan dolayı
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

# kontur bul, beyaz alan sınırı
cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

if len(cnts) == 0:
    print("Barkod bulunamadı.")
else:
    c = sorted(cnts, key=cv2.contourArea, reverse=True)[0] #en buyuk konturur sec

    # döndürülmüş bounding box, egik ise diye
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    box = box.astype(int)   

    cv2.drawContours(image, [box], -1, (0, 255, 0), 3) #yesil barkod kutusu ciz

    cv2.imshow("Barkod Tespiti", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
