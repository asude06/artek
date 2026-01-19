import argparse
import imutils
import cv2

# python nesneleri_saymak.py -i input.png

# Argüman ayrıştırıcısını oluşturun ve argümanları ayrıştırın
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
args = vars(ap.parse_args())

# Giriş görüntüsünü yükle (yol komut satırı aracılığıyla belirtilmiştir)
# argümanı) ve görüntüyü ekranımıza yansıtıyoruz.
image = cv2.imread(args["image"])
cv2.imshow("Image", image)
cv2.waitKey(0)

# Resmi gri tonlamaya dönüştür
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Gray", gray)
cv2.waitKey(0)

# kenarlar iç dış tümünü beyaz ile çerçeveler
edged = cv2.Canny(gray, 30, 150)
cv2.imshow("Edged", edged)
cv2.waitKey(0)

# Görüntüdeki tüm piksel değerlerini 225'ten küçük ayarlayarak eşikleme işlemi uygulayın.
# 255'e kadar (beyaz; ön plan) ve tüm piksel değerleri >= 225 ile 255 arasında
# (siyah; arka plan), böylece görüntüyü bölümlere ayırıyor.
thresh = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY_INV)[1]
cv2.imshow("Thresh", thresh)
cv2.waitKey(0)

# Ön plandaki nesnelerin konturlarını (yani dış hatlarını) bulun
# eşiklenmiş görüntü
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
output = image.copy()

# konturlar üzerinde döngü
for c in cnts:
    # Çıktı görüntüsündeki her bir konturu 3 piksel kalınlığında mor renkle çizin
	# Anahatı çizin, ardından çıktı konturlarını tek tek görüntüleyin.
	cv2.drawContours(output, [c], -1, (240, 0, 159), 3)
	cv2.imshow("Contours", output)
	
# Bulunan toplam kontur sayısını mor renkle çizin
text = "I found {} objects!".format(len(cnts))
cv2.putText(output, text, (10, 25),  cv2.FONT_HERSHEY_SIMPLEX, 0.7,
	(240, 0, 159), 2)
cv2.imshow("Contours", output)
cv2.waitKey(0)

# Ön plandaki nesnelerin boyutunu küçültmek için aşındırma işlemi uyguluyoruz.
mask = thresh.copy()
mask = cv2.erode(mask, None, iterations=5)
cv2.imshow("Eroded", mask)
cv2.waitKey(0)

# Benzer şekilde, genleşmeler yerdeki nesnelerin boyutunu artırabilir.
mask = thresh.copy()
mask = cv2.dilate(mask, None, iterations=5)
cv2.imshow("Dilated", mask)
cv2.waitKey(0)

# Uygulamak isteyebileceğimiz tipik bir işlem, maskemizi çıkarmak ve
# Giriş görüntümüze bit düzeyinde VE işlemi uygulayarak yalnızca maskelenmiş kısmı koruyalım.
# bölgeler
mask = thresh.copy()
output = cv2.bitwise_and(image, image, mask=mask)
cv2.imshow("Output", output)
cv2.waitKey(0)