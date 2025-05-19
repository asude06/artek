# 2 resmin birbirine eşitliğini kontrol edicez
# her bir renk pikselinin değeri eşitse o zaman bunlar aynı resim diyebiliriz
import cv2
import numpy as np

path = "aircraft.jpg"
path2 = "aircraft2.jpg"

img1 = cv2.imread(path)
img1 = cv2.resize(img1,(640,550))

img2 = cv2.imread(path2)
img2 = cv2.resize(img2,(640,550))

img3 = cv2.medianBlur(img1,7) #biraz bozunumladık ve fark belli oldu

if img1.shape == img2.shape:
    print("same size")
else:
    print("not same")

# diff = difference fark anlamına geliyor
diff = cv2.subtract(img1,img3) # farklı olan yerleri beyaza aynı olan yerleri siyaha boyuyor

b,g,r = cv2.split(diff)
# print(b) mavi değerleri

# cv2.countNonZero() # tarar, kaç tane sıfır olmadığını sayar
if cv2.countNonZero(b)==0 and cv2.countNonZero(g)==0 and cv2.countNonZero(r)==0:
    print("completely equal") # görselden belki fark anlaşılmaz diye sayısal değerlerini kıyaslayarak eşitliğini kanıtlıyoruz
else:
    print("not completely equal")

cv2.imshow("aircraft",img1)
cv2.imshow("aircraft2",img2)
cv2.imshow("diff",diff)

cv2.waitKey(0)
cv2.destroyAllWindows()