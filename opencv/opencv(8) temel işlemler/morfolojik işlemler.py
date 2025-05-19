import cv2
import numpy as np

img = cv2.imread("smile.jpg", 0)

kernel = np.ones((5,5),np.uint8) # bu matrisi üzerinde 5 kez uygulatıyor

# erosion = cv2.erode(img,kernel,iterations=1) # erozyona uğratıyor, inceltiyor, resmi bi bulanıklık var, iterasyon bozulmayı (siyahları) arttırıyor
# cv2.imshow("erosion",erosion)

# dilation = cv2.dilate(img,kernel,iterations=5)
# cv2.imshow("dilation",dilation) # kalınlaştırma (beyazı) uygulatıyor

# opening = cv2.morphologyEx(img,cv2.MORPH_OPEN,kernel) # resim üzerindeki bozulmaları düzeltiyor noktalar falan, ama bulurlu gibi yine de
# cv2.imshow("opening", opening)
#
# closing = cv2.morphologyEx(img,cv2.MORPH_CLOSE,kernel) # nesne içindeki bozulmaları düzeltiyormuş
# cv2.imshow("closing", closing)

gradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT,kernel) # nesne dışı beyaz içi siyah olarak bırakır
cv2.imshow("gradient",gradient)

# tophat = cv2.morphologyEx(img,cv2.MORPHOLOGY_TOPHAT,kernel)
# cv2.imshow("TOPHAT",tophat)

cv2.imshow("img",img)


cv2.waitKey(0)
cv2.destroyWindow()