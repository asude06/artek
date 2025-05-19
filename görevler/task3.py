
import cv2
import numpy as np

img = cv2.imread("C:\\Users\\Asus\\Desktop\\artek\\para2.jpeg")
img = cv2.resize(img, (640, 480))

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
clahe = cv2.createCLAHE(clipLimit=3.35, tileGridSize=(8,8))
gray = clahe.apply(gray)

img_blur = cv2.GaussianBlur(gray, (5,5), 0)

ret, thresh = cv2.threshold(img_blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

kernel = np.ones((3, 3), np.uint8)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

sure_bg = cv2.dilate(opening, kernel, iterations=20)

dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
_, sure_fg = cv2.threshold(dist_transform, 0.6 * dist_transform.max(), 255, 0)

sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg, sure_fg)

_, markers = cv2.connectedComponents(sure_fg)
markers = markers + 1
markers[unknown == 255] = 0

markers = cv2.watershed(img, markers)
img[markers == -1] = [0, 0, 255]

circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,dp=1,minDist=134.99,param1=100,param2=64,  minRadius=57,maxRadius=119)

if circles is not None:
    circles = np.uint16(np.around(circles))
    adet = len(circles[0])
    for i in circles[0, :]:
        cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
else:
    adet = 0

cv2.putText(img, 'Bulunan para sayisi: ' + str(adet), (110, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

cv2.imshow('img', img)
print(f"Görselde {adet} adet para bulundu")

cv2.waitKey(0)
cv2.destroyAllWindows()
