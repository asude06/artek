import numpy as np
import cv2

# #canvas = np.zeros((512,512,3), dtype = np.uint8)  # bgr --> 0 = siyah bir tuval oluşturur
# canvas = np.zeros((512,512,3), dtype = np.uint8) + 255  # bgr --> 255 = beyaz bir tuval oluşturuyor
# #canvas = np.zeros((512,512,3), dtype = np.uint8) + 100 # bgr --> acıl gri
# print(canvas)
#
# cv2.imshow("Canvas", canvas)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# piksel boyamak için yapılır
# boyanacak piksellerin boyutu bunlar
img = np.zeros((8,8,3),np.uint8) # 3. kanal verisi renkli resimler için o olmazsa siyah beyaz olur
img[0,0] = (255,255,255)
img[0,1] = (255,255,200)
img[0,2] = (255,255,150)
img[0,3] = (255,255,15)
img[0,4] = (15,255,255)
img[0,5] = (150,255,255)
img[0,6] = (200,255,255)
img[0,7] = (255,255,255)

# img = np.zeros((10,10),np.uint8)  # siyah beyaz renkler çünkü 3.kanal yok
# img[0,0] = 255
# img[0,1] = 200
# img[0,2] = 100
# img[0,3] = 15


img = cv2.resize(img, (1000,1000), interpolation=cv2.INTER_AREA) # üst üste gelmesinler diye

cv2.imshow("Canvas", img)
cv2.waitKey(0)
cv2.destroyAllWindows()



