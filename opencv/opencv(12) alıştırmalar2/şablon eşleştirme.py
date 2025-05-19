# elimizde bir şablon olacak resimde oşaplon var mı diye aratıcaz
#template = şablon resmin küçük bir parçası

import cv2
import numpy as np

image_path = "C:\\Users\\Asus\\Desktop\\artek\\starwars.jpg"
template_path = "C:\\Users\\Asus\\Desktop\\artek\\starwars2.jpg"

img = cv2.imread(image_path)
gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

template = cv2.imread(template_path,0) # 0 gri şekilde gösterecek / 1 yazsak old gibi gösterirdi
# gray_template = cv2.cvtColor(template,cv2.COLOR_BGR2GRAY)
# template = cv2.imread(template_path,cv2.IMREAD_GRAYSCALE) böyle de griye çevrilir

w,h = template.shape[::-1] #genişlik ve yükseklik al

# print(template.shape) # 2 bilgi veriyor boyutları ama renk bilgisi yok channel = 3 olurdu renkli olsaydı // renkli mi değil mi diye kontrol ediyoruz

result = cv2.matchTemplate(gray_img,template,cv2.TM_CCOEFF_NORMED)

location = np.where(result >= 0.95) # değerin konumunu veriyor

for point in zip(*location[::-1]): #yükseklik ve genişliği alır bir dizi verir zip olmasa, zip anlamlı koordinat verir
    cv2.rectangle(img,point,(point[0]+w,point[1]+h),(0,255,0),3)


#cv2.imshow("template",template)
#cv2.imshow("result",result) #beyaz nolta şablonun sol üst köşesi
cv2.imshow("image",img)

cv2.waitKey(0)
cv2.destroyAllWindows()