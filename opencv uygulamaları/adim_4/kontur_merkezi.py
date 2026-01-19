# python kontur_merkezi.py -i kontur_merkezi.jpg
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
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

# konturlar
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# tüm sekiller icin donecek
for c in cnts:
    # moment hesapla
    M = cv2.moments(c)

    # sıfıra bölme hatasını önlemek icin kosul
    if M["m00"] == 0:
        continue

    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
    cv2.putText(image, "center", (cX - 20, cY - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (255, 255, 255), 2)

    cv2.imshow("Image", image)
    cv2.waitKey(0)

cv2.destroyAllWindows()