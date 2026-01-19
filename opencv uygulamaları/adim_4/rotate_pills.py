import numpy as np
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to the image file")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
if image is None:
    raise IOError("Görüntü okunamadı! Dosya yolunu kontrol et.")

cv2.imshow("Original Image", image)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Gray", gray)

edged = cv2.Canny(gray, 30, 150)
cv2.imshow("Edged", edged)

# kontur bulma
cnts = cv2.findContours(edged.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# en buyuk knorue secerek
if len(cnts) > 0:
    c = max(cnts, key=cv2.contourArea)

    # maske oluştur
    mask = np.zeros(gray.shape, dtype="uint8")
    cv2.drawContours(mask, [c], -1, 255, -1)

    # bounding box ve ROI
    (x, y, w, h) = cv2.boundingRect(c)
    imageROI = image[y:y + h, x:x + w]
    maskROI = mask[y:y + h, x:x + w]

    imageROI = cv2.bitwise_and(imageROI, imageROI, mask=maskROI)
    cv2.imshow("ROI", imageROI)

    # kesilen
    for angle in np.arange(0, 360, 15):
        rotated = imutils.rotate(imageROI, angle)
        cv2.imshow("Rotated (Problematic)", rotated)
        cv2.waitKey(0)

    cv2.destroyAllWindows()

    # kesilmeyen
    for angle in np.arange(0, 360, 15):
        rotated = imutils.rotate_bound(imageROI, angle)
        cv2.imshow("Rotated (Correct)", rotated)
        cv2.waitKey(0)

else:
    print("Hiç kontur bulunamadı.")

cv2.destroyAllWindows()

# python rotate_pills.py -i input.png