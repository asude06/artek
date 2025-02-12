import cv2
import numpy as np

img = cv2.imread("smile.jpg")

dimension = img.shape
print(dimension)

color = img[336,483]
print("BGR: ",color)

blue = img[336,483,0]
print("blue: ",blue)

green = img[336,483,1]
print("green: ",green)

red = img[336,483,2]
print("red: ",red)

img[336,483,0] = 250  # mavinin değerini değiştirdik
print("new blue: ",img[336,483,0])

blue1 = img.item(150,200,0) # değer değiştirmek için bir yöntem
print("blue1: ",blue1)

img[150,200,0] = 172 # direkt indeks üzerinden değiştirdik yukardaki gibi

# img.itemset((150,200,0),172) #bu eski sürümde kalmış yenisind yok
print("new blue1: ",img[150,200,0])

cv2.imshow("smile",img)
cv2.waitKey(0)
cv2.destroyAllWindows()