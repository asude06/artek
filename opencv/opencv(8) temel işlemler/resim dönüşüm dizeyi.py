import cv2
import numpy as np

img = cv2.imread("smile.jpg", 0)
row,col = img.shape

# print(img.shape)
# print(row)
# print(col)

M= np.float32([[1,0,50],[0,1,200]])  # matris düzeyinde girdiğimiz değerler sol üst köşedeki açıklığı değiştirir o da resmin kaymasını etkiliyor

dst = cv2.warpAffine(img,M,(row,col))

cv2.imshow("dst",dst)
cv2.waitKey(0)
cv2.destroyAllWindows()