# python siyah_sekil_bulma.py -i sekiller.png
import numpy as np
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

# siyah renk maskesi

# BGR uzayında siyaha yakın pikseller
lower = np.array([0, 0, 0], dtype="uint8")
upper = np.array([15, 15, 15], dtype="uint8")

shapeMask = cv2.inRange(image, lower, upper)

# konturlar
cnts = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

print("I found {} black shapes".format(len(cnts)))

# maskeyi göster
cv2.imshow("Mask", shapeMask)
cv2.waitKey(0)

# konturları orijinal resimde cizip gosterir
for c in cnts:
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    cv2.imshow("Image", image)
    # cv2.waitKey(0)

cv2.waitKey(0)
cv2.destroyAllWindows()