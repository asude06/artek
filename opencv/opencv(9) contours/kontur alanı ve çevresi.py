import cv2

img = cv2.imread("contour.png")

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# bir görüntüyü eşikleme (thresholding) işlemine tabi tutar. Bu işlem, görüntüdeki pikselleri belirli bir eşik değerine göre siyah-beyaz (binary) veya farklı tonlara dönüştürerek basitleştirmeye yarar.

ret, thresh =cv2.threshold(gray,127,255, cv2.THRESH_BINARY) # THRESH_BINARY ,Eşik değerinin altında olanları siyah, üstünde olanları beyaz yapar.

contours,_ = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

#M = cv2.moments((contours[0]))
# print(M)

cnt = contours[0]

area = cv2.contourArea(cnt)  # alanı verir
print(area)

M = cv2.moments(cnt)
print(M['m00'])

perimeter = cv2.arcLength(cnt,True) # çevreyi verir
print(perimeter)

# cv2.imshow("orijinal",img)
# cv2.imshow("gray", gray)
# cv2.imshow("thresh",thresh)

cv2.waitKey(0)
cv2.destroyAllWindows()