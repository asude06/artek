import cv2
import numpy as np
import matplotlib.pyplot as plt

# path = "C:\\Users\\Asus\\Desktop\\artek\\smile.jpg"
# img = cv2.imread(path,0) # BGR
# #img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # yukarda 1 yazsaydık bu işlemi yapmak zorundaydık ama 0 old için gererk kalmıyor
# plt.imshow(img,cmap='gray',interpolation = 'BICUBIC') # RGB
# plt.show()

# bgr gelen resmi rgb yapmak cvt color yaparız

# path = "C:\\Users\\Asus\\Desktop\\artek\\smile.jpg"
# img = plt.imread(path)
# print(img)
# print("min value: ",img.min())
# print("max value: ", img.max())
# print("mean: ", img.mean())
# print("median: ",np.median(img))
# print("average: ",np.average(img))
# print("mean1: ",np.mean(img))

################################

# path = "C:\\Users\\Asus\\Desktop\\artek\\map.jpeg"
# img = plt.imread(path)


"""
[r,g,b]
[50,50,0]
[70,70,1]
[:,:,2]
r -> 0-255
g -> 0-255
b -> 0-255 
"""

# r = img[:,:,0]
# g = img[:,:,1]
# b = img[:,:,2]

# output = np.dstack((r,g,b))
# plt.imshow(output)
# plt.show()

# output = [img,r,g,b]
# titles = ["Image","Red","Green","Blue"]
#
# for i in range(4):
#     plt.subplot(2,2,i+1) #alt grafikler oluşturmak
#     plt.axis("off")
#     plt.title(titles[i])
#     if i ==0:
#         plt.imshow(output[i])
#     else:
#         plt.imshow(output[i],cmap='gray')
#     plt.show()

########################################

img = plt.imread("C:\\Users\\Asus\\Desktop\\artek\\map.jpeg")

plt.subplot(4,2,1)
plt.title("Original Image")
plt.imshow(img)

plt.subplot(4,2,2)
plt.title("img+img")
plt.imshow(img+img)

plt.subplot(4,2,3)
plt.title("img-img")
plt.imshow(img-img)

plt.subplot(4,2,4)
plt.title("np.flip(img,0)")
plt.imshow(np.flip(img,0)) #0,1,2

plt.subplot(4,2,5)
plt.title("np.flip(img,1)")
plt.imshow(np.flip(img,1)) #0,1,2


plt.subplot(4,2,6)
plt.title("np.flip(img,2)")
plt.imshow(np.flip(img,2)) #0,1,2

plt.subplot(4,2,7)
plt.title("np.fliplr(img)") # left to right
plt.imshow(np.fliplr(img))

plt.subplot(4,2,8)
plt.title("np.flipud(img)") # updown
plt.imshow(np.flipud(img))

plt.show()
