import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
if image is None:
    raise IOError("Görüntü okunamadı! Dosya yolunu kontrol et.")

# renk sınırları BGR
boundaries = [
    ([17, 15, 100], [50, 56, 200]), #kırmızıya yakın olan renkeler secilecek
    ([86, 31, 4], [220, 88, 50]),
    ([25, 146, 190], [62, 174, 250]),
    ([103, 86, 65], [145, 133, 128])
]

# sınırlar üzerinden döndürme
for (lower, upper) in boundaries:
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    # maske oluştur
    mask = cv2.inRange(image, lower, upper)

    # maske uygula
    output = cv2.bitwise_and(image, image, mask=mask)

    # orijinal + filtrelenmiş görüntüyü yan yana göster
    combined = np.hstack([image, output])
    cv2.imshow("Original | Color Mask", combined)
    cv2.waitKey(0)

cv2.destroyAllWindows()
# python renk_filtreleme.py -i renk_filtreleme.jpg