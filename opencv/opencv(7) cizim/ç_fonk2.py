import numpy as np
import cv2
from unicodedata import mirrored

canvas = np.zeros((1024,1024, 3), dtype=np.uint8) + 255


# çizgi
# cv2.line(canvas, (50,50),(512,512),(250,0,0),thickness=5) # başlayacağı, biteceği, rengi, kalınlık
# cv2.line(canvas, (100,50),(200,250),(0,0,250),thickness=7) # başlayacağı, biteceği, rengi, kalınlık

# düzgün dörtgen
# cv2.rectangle(canvas, (20,20), (50,50), (0,255,0), thickness=-1) # - li değe içini dolduruyor
# cv2.rectangle(canvas, (50,50), (150,150), (0,255,0), thickness=-1) # - li değe içini dolduruyor

# # çember
# cv2.circle(canvas, (250,250), 100, (0,0,250),thickness=-1)
#
# # üçgen
# p1 = (100,200)
# p2 = (50,50)
# p3 = (300,100)
#
# cv2.line(canvas, p1, p2, (0,0,0),4)
# cv2.line(canvas, p2, p3, (0,0,0),4)
# cv2.line(canvas, p1, p3, (0,0,0),4)
#
# # düzgün olmayan dörtgen
#
# points = np.array([[[110,200],[330,200],[290,220],[100,100]]],np.int32)
# cv2.polylines(canvas, [points], True, (0,0,100),5)
# #           merkez noktası   genişlik   yükseklik , başlangıc-bitiş açıları
# cv2.ellipse(canvas, (300,300), (80,20), 10, 90, 360, (255,255,0),-1)

########################################################################################################


# cv2.rectangle(canvas, (50,50), (100,100), (50,0,80), thickness=-1) # - li değer içini dolduruyor
# cv2.rectangle(canvas, (100,100), (150,150), (50,50,150), thickness=-1) # - li değer içini dolduruyor
# cv2.rectangle(canvas, (150,150), (200,200), (50,50,0), thickness=-1)
# cv2.rectangle(canvas, (200,200), (250,250), (50,50,50),thickness=-1)
# cv2.rectangle(canvas, (250,250), (300,300), (124,195,116),thickness= -1)
# cv2.rectangle(canvas, (300,300), (350,350), (70,144,218), thickness=-1)
# cv2.rectangle(canvas, (350,350), (400,400), (172,144,14), thickness=-1)

colors = [
    (50, 0, 80),     # Mor
    (50, 50, 150),   # Mavi-mor
    (50, 50, 0),     # Zeytin yeşili
    (50, 50, 50),    # Gri
    (124, 195, 116), # Açık yeşil
    (70, 144, 218),  # Açık mavi
    (172, 144, 14)   # Hardal sarısı
]

# Tuvalin genişliği (simetri için kullanacağız)
width = canvas.shape[1]

# Karelerin başlangıç noktası
start_x = 100  # Sol taraftaki ilk kare nerede başlayacak?
start_y = 100  # Üstten itibaren başlangıç noktası
size = 50      # Her bir karenin boyutu

for i, color in enumerate(colors):
    x1 = start_x + (i * size)
    y1 = start_y + (i * size)
    x2 = x1 + size
    y2 = y1 + size

    # Orijinal kareyi çiz
    cv2.rectangle(canvas, (x1, y1), (x2, y2), color, thickness=-1)

    # Y eksenine göre simetri al (ayna görüntüsü)
    mirrored_x1 = width - x2
    mirrored_x2 = width - x1

    # Yansıtılmış kareyi çiz
    cv2.rectangle(canvas, (mirrored_x1, y1), (mirrored_x2, y2), color, thickness=-1)

cv2.circle(canvas, (512,500), 80, (200,100,250),thickness=-1)
cv2.circle(canvas, (512,629), 50, (137,80,250),thickness=-1)

cv2.imshow("Canvas", canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()