import cv2
import numpy as np
import imutils
from skimage.filters import threshold_local


IMAGE_PATH = "optik.jpg"   

def order_points(pts):  # görselin köselerini doğru olacak sekilde sıralar, düz bi görüntü icin
    rect = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]     # sol-ust , en kücük
    rect[2] = pts[np.argmax(s)]     # sag-alt , en buyuk

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]  # sag-ust
    rect[3] = pts[np.argmax(diff)]  # sol-alt

    return rect


def four_point_transform(image, pts): # perspektifliyi kusbakisina donusturur
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    widthA = np.linalg.norm(br - bl) #alt kenar uzunlugu
    widthB = np.linalg.norm(tr - tl) #ust kenar uzunlugu
    maxWidth = int(max(widthA, widthB))

    heightA = np.linalg.norm(tr - br) #sol yukseklik
    heightB = np.linalg.norm(tl - bl) #sag yukseklik
    maxHeight = int(max(heightA, heightB))

    dst = np.array([  # noktalariverilen resme gore yeniden duzenler
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight)) # kusbakısı burda olusturuluyor

    return warped


# Adım 1: Kenar Bulma 

image = cv2.imread(IMAGE_PATH)
orig = image.copy()
ratio = image.shape[0] / 500.0 #yeniden olcekleme orani, boyut degistimesi yapacagiz 

image = imutils.resize(image, height=500) #kuculturuz daha az islem icin

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # gray faormatta inceleme yaptırırız
gray = cv2.GaussianBlur(gray, (5, 5), 0) #gürültü azaltma 
edged = cv2.Canny(gray, 75, 200) # kenarlari isaretler

cv2.imshow("Image", image)
cv2.imshow("Edged", edged)

# Adım 2: Kontur Bulma 

cnts = cv2.findContours(edged.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE) # tum konturları bulur, aynı nokta üzerinedkşlerşi tek cizgiye indirger
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5] #konturlardan secme yapar ilk 5

screenCnt = None

for c in cnts:
    peri = cv2.arcLength(c, True) #kontur cevre uzunlugu
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    if len(approx) == 4: # 4 koseli olan kontur
        screenCnt = approx
        break

if screenCnt is None:
    raise Exception("Belge konturu bulunamadı!")

cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2) # yesil ile tespit edilen tam sarmlar
cv2.imshow("Outline", image)

# Adım 3: Perspektif Dönüşümü ve Threshold 

warped = four_point_transform( #düz belge seklinde cıktı verir
    orig,
    screenCnt.reshape(4, 2) * ratio
)

warped_gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)

#görüntüyü siyah beyaz yaprken bölgesiine göre bir eşikleme yaptırıyoruz
T = threshold_local(warped_gray, 11, offset=10, method="gaussian")
warped_thresh = (warped_gray > T).astype("uint8") * 255 #metinler siyah, arka beyaz, scan efekt

#cv2.imshow("Original", imutils.resize(orig, height=650))
cv2.imshow("Scanned", imutils.resize(warped_thresh, height=650))
cv2.waitKey(0)
cv2.destroyAllWindows()