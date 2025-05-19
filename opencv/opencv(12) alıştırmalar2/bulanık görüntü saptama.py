import cv2

img = cv2.imread("aircraft.jpg")
blurry_img = cv2.medianBlur(img,7) #burdaki değer arttıkça yani blur arttıkça laplacian değeri artıyor

laplacian = cv2.Laplacian(blurry_img,cv2.CV_64F).var() # değer belli bir değerin altındaysa blurlu deriz

print(laplacian)

if laplacian < 60:
    print("blurry image")


cv2.imshow("img",img)
cv2.imshow("blurry_img",blurry_img)

cv2.waitKey(0)
cv2.destroyAllWindows()
