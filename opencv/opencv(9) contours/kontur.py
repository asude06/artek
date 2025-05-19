# şeklin çevre çizgileri , sınırçizgilerini belirlemek

# önce griye cvt ile sonra binary r threshold ile dönüştürülür

# alan, çevre, geometrik merkezi, çevreleyici geometriler

# konveks = dışbükey, convex hull örtü içbükeyi dışbükey ile örtmek

#dışbükey kusurlar (defects)  mesela elin tanımlanması parmaklar alan
#kusurları sayarak kaç gösterdiğini bildiriyor

import cv2

img = cv2.imread("contour1.png")

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

_,thresh= cv2.threshold(gray,127,255,cv2.THRESH_BINARY)

contours,_=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#print(contours)  # koordinatları veriyor

cv2.drawContours(img, contours, -1, (0,0,255),3)

cv2.imshow("contour",img)  # yukarda -1 dedik diye, hem şekli hem de tuvali çerçevelemiş, 0 olda sadece tuval içini çerçevelerdi
cv2.waitKey(0)
cv2.destroyAllWindows()

