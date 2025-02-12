import cv2
import numpy as np

circle = np.zeros((512,512,3), np.uint8) + 255
cv2.circle(circle, (256,256),60, (255,0,0),-1)  # tamamen mavi

rectangle = np.zeros((512,512,3),np.uint8) +255
cv2.rectangle(rectangle, (150,150), (350,350),(0,0,255),-1)  # tamamen kırmızı

cv2.imshow("circle",circle)
cv2.imshow("rectangle",rectangle)

add = cv2.add(circle,rectangle)  # mavi ve kırmızıyı topladı magenta renkli bir circle oluştu
print(add[256,256])

cv2.imshow("toplam",add)

cv2.waitKey(0)
cv2.destroyAllWindows()