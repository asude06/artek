import cv2
import numpy
import matplotlib

img = cv2.imread("smile.jpg", 0)  # resmi gri tonlarında verir 0 = GRİ
#img = cv2.imread("smile.jpg")  # resmi normal renkleriyle verir
#print(img)

cv2.namedWindow("image", cv2.WINDOW_NORMAL)  # resmi kenarlarından boyutunu değiştirmek için yapıyoruz

img = cv2.resize(img,(640,480)) # istediğimiz boyutlarda veriyor bize

cv2.imshow("image",img)
cv2.imwrite("smile.jpg", img) # resmi kaydetmek için kullanıyoruz

cv2.waitKey(0)  #sen kapatana kada durur, diğer türlü milisaniye cinsinden hesaplıyor

cv2.destroyAllWindows() # çıktığında tüm pencereleri kapatıyor



