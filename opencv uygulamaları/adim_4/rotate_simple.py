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
    raise IOError("Görüntü okunamadı! Dosya yolu veya adı yanlış.")

# kesilen yani kırpılmış
for angle in np.arange(0, 360, 15):
    rotated = imutils.rotate(image, angle)
    cv2.imshow("Rotated (Problematic)", rotated)
    cv2.waitKey(0)

def rotate_bound(image, angle):
    # görüntü boyutları ve merkez
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    # dönüş matrisi
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # yeni sınır boyutları
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # merkezi ayarla
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    return cv2.warpAffine(image, M, (nW, nH))

# kesilmeyen yani kırpılmamış
for angle in np.arange(0, 360, 15):
    rotated = rotate_bound(image, angle)
    cv2.imshow("Rotated (Correct)", rotated)
    cv2.waitKey(0)

cv2.destroyAllWindows()

# python rotate_simple.py -i input.jpg
