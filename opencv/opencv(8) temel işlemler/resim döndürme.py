import cv2
import numpy as np

# geometrik işlemler matrise dayanıyor

img = cv2.imread("smile.jpg", 0)
row,col = img.shape

#M= cv2.getRotationMatrix2D((col/2,row/2),90,1) # 90 derece + yönde döndürdü
M= cv2.getRotationMatrix2D((col/5,row/3),180,1) # böldüğümüz satır ve sütun sayılarını o oranda azalttı gibi, en sondakibüyürse de yaklaştırılmış olur
dst = cv2.warpAffine(img,M,(col,row))

cv2.imshow("dst",dst)

cv2.waitKey(0)
cv2.destroyAllWindows()