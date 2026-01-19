import imutils
import cv2

image = cv2.imread("jp.jpg")
(h, w, d) = image.shape
print("width={}, height={}, depth={}".format(w, h, d))

( B, G, R ) = image [ 100 , 50 ] #x=50 ve y=100 deki piselin bgr degerlerini bize döndurur
print ( "R={}, G={}, B={}" . format ( R, G, B ))

# x=270,y=40 noktasından başlayıp x=350,y=140 noktasında biten giriş görüntüsü
roi = image[40:140, 270:350] # y nin ve x in basla-bitis
# cv2.imshow("ROI", roi)

resized = cv2.resize(image, (200, 200)) #resmin boyutlarını x de 200 y de 200 olacak şekilde degistirr, sıkısmıs gibi gözükür
# cv2.imshow("Fixed Resizing", resized)

# Sabit yeniden boyutlandırma ve en boy oranı bozulması nedeniyle genişliği yeniden boyutlandıralım.
# Yüksekliği 300 piksel olarak ayarlayın ancak yeni yüksekliği en boy oranına göre hesaplayın
r = 300.0 / w
dim = (300, int(h * r))
resized = cv2.resize(image, dim)
# cv2.imshow("Aspect Ratio Resize", resized)

# Öncelikle OpenCV kullanarak bir görüntüyü saat yönünde 45 derece döndürelim.
# Görüntü merkezini hesaplamak, ardından döndürme matrisini oluşturmak,
# ve son olarak afin çarpıtmayı uygulamak
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, -45, 1.0)
rotated = cv2.warpAffine(image, M, (w, h))
# cv2.imshow("OpenCV Rotation", rotated)

# OpenCV, döndürülen görüntümüzün döndürme sonrasında kırpılıp kırpılmadığını "önemsemiyor".
# böylece bunun yerine imutils'in başka bir kolaylık fonksiyonunu kullanabiliriz.
# bizi dışarı
rotated = imutils.rotate_bound(image, 45)
# cv2.imshow("Imutils Bound Rotation", rotated)

# Görüntüyü yumuşatmak için 11x11 çekirdekli Gauss bulanıklığı uygulayın,
# Yüksek frekanslı gürültüyü azaltırken kullanışlıdır
blurred = cv2.GaussianBlur(image, (11, 11), 0)
# cv2.imshow("Blurred", blurred)

# Yüzü çevreleyen 2 piksel kalınlığında kırmızı bir dikdörtgen çizin
output = image.copy()
cv2.rectangle(output, (270, 40), (350, 140), (0, 0, 255), 2)
# cv2.imshow("Rectangle", output)

# Resmin ortasına 20 piksel çapında (içi dolu) mavi bir daire çizin
# x=300,y=150
output = image.copy()
cv2.circle(output, (250, 150), 20, (255, 0, 0), -1)
# cv2.imshow("Circle", output)

# x=60,y=20 noktasından x=400,y=200 noktasına 5 piksel kalınlığında kırmızı bir çizgi çizin
output = image.copy()
cv2.line(output, (60, 20), (400, 200), (0, 0, 255), 5)
# cv2.imshow("Line", output)

# Resmin üzerine yeşil metin çiz
output = image.copy()
cv2.putText(output, "OpenCV + Jurassic Park!!!", (10, 25), 
	cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
cv2.imshow("Text", output)

cv2.imshow("Image", image)
cv2.waitKey(0)