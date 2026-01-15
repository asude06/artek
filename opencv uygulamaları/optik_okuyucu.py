from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import imutils
import cv2


IMAGE_PATH = "optik.jpg"  

# Cevap anahtari 
# 0:A 1:B 2:C 3:D 4:E
ANSWER_KEY = {
    0: 1,  # B
    1: 4,  # E
    2: 0,  # A
    3: 3,  # D
    4: 1   # B
}

# adım 1: resimden kenar tespiti

image = cv2.imread(IMAGE_PATH)

if image is None:
    raise Exception("Optik form yüklenemedi! Dosya yolunu kontrol et.")


gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0) #gürültü azaltır kücük gereksiz şeyleri 
edged = cv2.Canny(blurred, 75, 200) # ani parlaklık degisimlerini hesaplar çizgiler kenarlar belirginleşir

# adim 2: dıs sınır tespti
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) # kapalı şekillerin konturlarını bulur, sadece en dıştaki konturu al, gereksiz noktaları siler

cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

docCnt = None
for c in cnts:
    peri = cv2.arcLength(c, True) # kontur cevresini hesaplar
    approx = cv2.approxPolyDP(c, 0.02 * peri, True) #yaklasım hassasiyeti
    if len(approx) == 4: # dortgen
        docCnt = approx
        break

if docCnt is None:
    raise Exception("Belge bulunamadı!")

# adim 3: perspektif donsumu
paper = four_point_transform(image, docCnt.reshape(4, 2)) # 4 nokra 2 koordinat formuna cevirir
warped = four_point_transform(gray, docCnt.reshape(4, 2)) # baloncuk analizi

# adım 4: THRESHOLD 
thresh = cv2.threshold(
    warped, 0, 255,
    cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU #dolu baloncuk beyaz , arka plan siyah, osu oto eşik seçimi
)[1]

# adim 5: baloncuk konturu bulma
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #Tüm bağımsız beyaz bölgeler bulunuyor
cnts = imutils.grab_contours(cnts)

questionCnts = [] #baloncuk olan konturları tutacak
for c in cnts:
    (x, y, w, h) = cv2.boundingRect(c) # konturu saran en kucuk dortgen olusturacak, daire icin genislik=yuksekleik
    ar = w / float(h) # daireye yakın sekilleri hesaplar, yaklaşık 1 e esitse mükkmel daire

    if w >= 20 and h >= 20 and 0.9 <= ar <= 1.1:
        questionCnts.append(c)

# adim 6: balncukları sırala ve cevapları degerlendir

questionCnts = contours.sort_contours(questionCnts,method="top-to-bottom")[0] #soruları satır satır alır

correct = 0 #toplam dogru cevap sayisi

for (q, i) in enumerate(range(0, len(questionCnts), 5)): # her 5 baloncuk 1 soru demek
    cnts = contours.sort_contours(
        questionCnts[i:i + 5])[0] # sorunun sıklarını srıalar

    bubbled = None #en cok doldurulan baloncuk

    for (j, c) in enumerate(cnts): #her sık icin doluluk ölcumu
        mask = np.zeros(thresh.shape, dtype="uint8")
        cv2.drawContours(mask, [c], -1, 255, -1) #sadece o baloncugun icini beyaz yap, diger yerler siyah

        mask = cv2.bitwise_and(thresh, thresh, mask=mask) #maskeyi esikleme sadecebaloncuk icindeki siyah/beyaz doluluk oranı kalır
        total = cv2.countNonZero(mask) #Ne kadar çok siyah pikselse o kadar dolu

        if bubbled is None or total > bubbled[0]: # en dolsunu sec
            bubbled = (total, j)

    color = (0, 0, 255) #yanlısa kırmızı olacak
    k = ANSWER_KEY[q] # dogru sııkın indeksi

    if k == bubbled[1]:
        color = (0, 255, 0) # dogruysa yesil yap
        correct += 1

    cv2.drawContours(paper, [cnts[k]], -1, color, 3)

# adım 7: skor yazısı
score = (correct / len(ANSWER_KEY)) * 100 #yuzdelik basari orani
print(f"[INFO] Score: {score:.2f}%")

cv2.putText(paper, f"{score:.2f}%", #yazılacak metin
            (10, 30), #sol ustteki konum
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9, (0, 0, 255), 2) #yazı bıyutu , renk , kalınlık

cv2.imshow("Original", image)
cv2.imshow("Exam", paper)
cv2.waitKey(0)
cv2.destroyAllWindows()