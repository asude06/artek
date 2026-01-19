import argparse
import imutils
import cv2

# terminalde yazman gereken: python sekil_say.py -i input.png -o output.png

ap = argparse.ArgumentParser(description="Görüntüdeki şekilleri say")
ap.add_argument(
    "-i", "--input",
    required=True,
    help="Giriş görüntüsünün yolu"
)
ap.add_argument(
    "-o", "--output",
    required=True,
    help="Çıktı görüntüsünün yolu"
)

args = vars(ap.parse_args())

image = cv2.imread(args["input"])

if image is None:
    raise IOError("Giriş görüntüsü okunamadı. Dosya yolunu kontrol et.")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

cnts = cv2.findContours(
    thresh.copy(),
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)
cnts = imutils.grab_contours(cnts)

for c in cnts:
    cv2.drawContours(image, [c], -1, (0, 0, 255), 2)

text = "Toplamda {} sekil buldum".format(len(cnts))
cv2.putText(
    image,
    text,
    (10, 25),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.7,
    (0, 0, 255),
    2
)

cv2.imwrite(args["output"], image)

print("Bulunan sekil sayisi:", len(cnts))

cv2.imshow("Sonuc", image)
cv2.waitKey(0)
cv2.destroyAllWindows()