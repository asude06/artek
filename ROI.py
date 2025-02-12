# roi --> region of intrest  --> ilgi alanı

import cv2

img = cv2.imread("smile.jpg")

print(img.shape[:2]) # resmin boyutlarını görmek için yazıyoruz

roi = img[150:250 , 230:400]  #sadece belli aralıkları taratır ve ordaki görüntüyü bize yansıtır

cv2.imshow("smile",img)
cv2.imshow("roi",roi)

cv2.waitKey(0)
cv2.destroyAllWindows()
