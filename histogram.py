import cv2
import numpy as np
from matplotlib import pyplot as plt

# resmin piksel grafiğini oluşturuyor
# grafik gibi düşün, değer yoğunlukları hakkında çıkarımlarda bulunabiliriz

# img = np.zeros((500,500),np.uint8)
#
# cv2.rectangle(img,(0,60),(200,150),(255,255,255),-1)
# cv2.rectangle(img,(250,170),(350,200),(255,255,255),-1)

img = cv2.imread("smile.jpg")

b,g,r = cv2.split(img)

cv2.imshow("img",img)

# plt.hist(img.ravel(),256,[0,256]) # ravel diziye döküyor değerleri
# plt.show()

# 3 farklı rengin hisi tek bir grafikte
plt.hist(b.ravel(),256,[0,256])
plt.hist(g.ravel(),256,[0,256])
plt.hist(r.ravel(),256,[0,256])

plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()