# birden fazla resim olan klasörden resimleri kırpıyır
from imutils import build_montages
from imutils import paths
import argparse
import random
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True,
                help="görüntülerin bulunduğu klasör yolu")
ap.add_argument("-s", "--sample", type=int, default=21,
                help="rastgele seçilecek görüntü sayısı")
args = vars(ap.parse_args())

imagePaths = list(paths.list_images(args["images"]))

# Rastgele karıştır
random.shuffle(imagePaths)

# İstenen sayıda seç
imagePaths = imagePaths[:args["sample"]]

images = []

for imagePath in imagePaths:
    image = cv2.imread(imagePath)
    if image is not None:
        images.append(image)

# Montaj oluştur (tek resim boyutu: 128x196, düzen: 7x3)
montages = build_montages(images, (128, 196), (7, 3))

# Montajları göster
for montage in montages:
    cv2.imshow("Montage", montage)
    cv2.waitKey(0)

cv2.destroyAllWindows()