# python uc_noktalari_bulma.py -i uc_noktalari_bulma.webp
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="giriş görüntüsünün yolu")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])

if image is None:
    raise IOError("Görüntü okunamadı. Dosya yolunu kontrol et.")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)

thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
thresh = cv2.erode(thresh, None, iterations=2)
thresh = cv2.dilate(thresh, None, iterations=2)

# konturlar
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

if len(cnts) == 0:
    raise RuntimeError("Hiç kontur bulunamadı.")

# en büyük konturu al
c = max(cnts, key=cv2.contourArea)

#uc noktalar
extLeft  = tuple(c[c[:, :, 0].argmin()][0])
extRight = tuple(c[c[:, :, 0].argmax()][0])
extTop   = tuple(c[c[:, :, 1].argmin()][0])
extBot   = tuple(c[c[:, :, 1].argmax()][0])

cv2.drawContours(image, [c], -1, (0, 255, 255), 2)
cv2.circle(image, extLeft,  8, (0, 0, 255), -1)     # sol (kırmızı)
cv2.circle(image, extRight, 8, (0, 255, 0), -1)     # sağ (yeşil)
cv2.circle(image, extTop,   8, (255, 0, 0), -1)     # üst (mavi)
cv2.circle(image, extBot,   8, (255, 255, 0), -1)   # alt (sarı)

cv2.imshow("Extreme Points", image)
cv2.waitKey(0)
cv2.destroyAllWindows()