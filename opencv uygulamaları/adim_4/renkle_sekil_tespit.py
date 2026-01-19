# python renkle_sekil_tespit.py -i kontur_merkezi.jpg
from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
import argparse
import imutils
import cv2

class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, c):
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True) #konturu köşelere indirger

        if len(approx) == 3:
            shape = "triangle"

        elif len(approx) == 4:
            (x, y, w, h) = cv2.boundingRect(approx) #kare dörtgen ayrımı yapmak icin
            ar = w / float(h)
            shape = "square" if 0.95 <= ar <= 1.05 else "rectangle"

        elif len(approx) == 5:
            shape = "pentagon"

        else:
            shape = "circle"

        return shape

class ColorLabeler:
    def __init__(self):
        colors = OrderedDict({ #renk sözlügü
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255)
        })

        self.lab = np.zeros((len(colors), 1, 3), dtype="uint8")
        self.colorNames = []

        for (i, (name, rgb)) in enumerate(colors.items()):
            self.lab[i] = rgb
            self.colorNames.append(name)

        self.lab = cv2.cvtColor(self.lab, cv2.COLOR_RGB2LAB)

    def label(self, image, c):
        mask = np.zeros(image.shape[:2], dtype="uint8") #kontur maskesi şeklin old yer beyaz
        cv2.drawContours(mask, [c], -1, 255, -1)
        mask = cv2.erode(mask, None, iterations=2)

        mean = cv2.mean(image, mask=mask)[:3] # şeklin içindeki ortalama lab rengi

        minDist = (np.inf, None)
        for (i, row) in enumerate(self.lab):
            d = dist.euclidean(row[0], mean)
            if d < minDist[0]:
                minDist = (d, i)

        return self.colorNames[minDist[1]]

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="giriş görüntüsünün yolu")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
if image is None:
    raise IOError("Görüntü okunamadı")

resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])

blurred = cv2.GaussianBlur(resized, (5, 5), 0)
gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]

cnts = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #dış konturlar
cnts = imutils.grab_contours(cnts)

sd = ShapeDetector()
cl = ColorLabeler()

for c in cnts:
    M = cv2.moments(c)
    if M["m00"] == 0:
        continue

    cX = int((M["m10"] / M["m00"]) * ratio)
    cY = int((M["m01"] / M["m00"]) * ratio) #şeklin merkezi

    shape = sd.detect(c)
    color = cl.label(lab, c)

    c = c.astype("float")
    c *= ratio #kucuk resimde bulunanlar buyuge tasınır
    c = c.astype("int")

    text = "{} {}".format(color, shape)
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    cv2.putText(image, text, (cX - 40, cY),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (255, 255, 255), 2)

cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()