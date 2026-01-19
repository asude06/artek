# python kontur_say.py -i kontur_say.jpg -m left-to-right
import numpy as np
import argparse
import imutils
import cv2

def sort_contours(cnts, method="left-to-right"): #kontuları soldan saga dogru sıralar
    reverse = False
    i = 0

    if method in ("right-to-left", "bottom-to-top"): # x buyukten kucuge
        reverse = True

    if method in ("top-to-bottom", "bottom-to-top"): # y buyukten kucuge
        i = 1

    boundingBoxes = [cv2.boundingRect(c) for c in cnts] # her kontur icin Sol üst köşe + genişlik + yükseklik
    (cnts, boundingBoxes) = zip(
        *sorted(zip(cnts, boundingBoxes),
                key=lambda b: b[1][i],
                reverse=reverse)
    )

    return cnts, boundingBoxes

def draw_contour(image, c, i): # kontur üzerine numarasını yazar
    M = cv2.moments(c) # alan, agırlık merkezi
    if M["m00"] == 0: #sıfıra bölme hatası olmaması icin
        return image

    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    cv2.putText(
        image,
        "#{}".format(i + 1),
        (cX - 20, cY),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (255, 255, 255),
        2
    )

    return image

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="giriş görüntüsünün yolu")
ap.add_argument("-m", "--method", required=True,
                help="sıralama yöntemi: left-to-right, right-to-left, top-to-bottom, bottom-to-top")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
if image is None:
    raise IOError("Görüntü okunamadı. Dosya yolunu kontrol et.")

# kenar haritası olusturma
accumEdged = np.zeros(image.shape[:2], dtype="uint8") #siyah boş bir maske

for chan in cv2.split(image): # gütültü azaltır kenarları bulur
    chan = cv2.medianBlur(chan, 11)
    edged = cv2.Canny(chan, 50, 200)
    accumEdged = cv2.bitwise_or(accumEdged, edged) #tüm kanallar tek haritada

cv2.imshow("Edge Map", accumEdged)

# konturlar
cnts = cv2.findContours(accumEdged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) # sadece dış konturlar
cnts = imutils.grab_contours(cnts)

if len(cnts) == 0:
    raise RuntimeError("Hiç kontur bulunamadı.")

# en büyük 5 konturu al
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

# sırasız kontur, bulundugu sıraya göre sıralama
orig = image.copy()
for (i, c) in enumerate(cnts):
    orig = draw_contour(orig, c, i)

cv2.imshow("Unsorted", orig)

# sıralı kontur, konuma göre yeniden sıralma
(cnts, boundingBoxes) = sort_contours(cnts, method=args["method"])

for (i, c) in enumerate(cnts):
    draw_contour(image, c, i)

cv2.imshow("Sorted", image)
cv2.waitKey(0)
cv2.destroyAllWindows()