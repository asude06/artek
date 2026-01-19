# python sekil_tespit.py -i kontur_merkezi.jpg
import cv2
import argparse
import imutils

class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, c): # kose sayısına gore tespit 
        # varsayılan şekil
        shape = "unidentified"

        # kontur çevresi
        peri = cv2.arcLength(c, True)

        # konturu yaklaştır (approximation)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True) #daha az koseli hale getirir

        # köşe sayısına göre sınıflandırma
        if len(approx) == 3:
            shape = "triangle"

        elif len(approx) == 4:
            # dikdörtgen mi kare mi?
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            shape = "square" if 0.95 <= ar <= 1.05 else "rectangle"

        elif len(approx) == 5:
            shape = "pentagon"

        else:
            shape = "circle" # 5 ten çok kosei varsa daire

        return shape

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="giriş görüntüsünün yolu")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
if image is None:
    raise IOError("Görüntü okunamadı")

resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])

gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1] #acik renkler beyaz koyular siyah

#konturlar
cnts = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

sd = ShapeDetector()

# konturları isle
for c in cnts:
    # şekli tespit et
    shape = sd.detect(c)

    # kontur merkezini bulur etiket yazmak icin, agırlık merkezi yani tam ortası
    M = cv2.moments(c)
    if M["m00"] == 0:
        continue

    cX = int((M["m10"] / M["m00"]) * ratio)
    cY = int((M["m01"] / M["m00"]) * ratio)

    # konturu orijinal ölçeğe geri al
    c = c.astype("float")
    c *= ratio
    c = c.astype("int")

    # çizimler
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    cv2.putText(image, shape, (cX - 40, cY),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (255, 255, 255), 2)

cv2.imshow("Shape Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()