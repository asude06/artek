import cv2
import numpy as np
import math

image = cv2.imread("dart5.jpeg")
if image is None:
    raise Exception("Resim yüklenemedi")

output = image.copy() #sonucları cizecegimiz bir kopya gerekli
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#dart sınırlarını buluyoruz adaptive (her bölgeye yerel eşik)
# Adaptive threshold (zayıf siyah çizgiler için)
black_mask = cv2.adaptiveThreshold(
    gray,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY_INV,
    31,
    5
) # siyah yerler beyaz olurdigerleri siyzh

# kenar(ince halkalar için)
edges = cv2.Canny(gray, 50, 150)

# halkaları tespit ederken direkt siyah renk üzeriinden yaptık ünkü griler karıştırıyordu
black_mask = cv2.bitwise_or(black_mask, edges) # ya thresle ya da ince kenar ile bulduysa tamam

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
black_mask = cv2.morphologyEx(black_mask, cv2.MORPH_CLOSE, kernel) 

cnts_rings, _ = cv2.findContours(
    black_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE # halkalari hiyerarşik yakalar
)

raw_ellipses = []

for c in cnts_rings:
    if len(c) < 100:
        continue

    area = cv2.contourArea(c)
    if area < 1500:
        continue

    if len(c) < 5:
        continue

    ellipse = cv2.fitEllipse(c) #dart halkaları elipse benziyor, onun ozellikleriyle modelleriz
    raw_ellipses.append(ellipse)

# ÇİFT ÇİZGİLERİ BİRLEŞTİR, canny altlı üstlü buluyor puan bölgesi karışıyordu
merged = []
used = [False]*len(raw_ellipses)

for i, e1 in enumerate(raw_ellipses):
    if used[i]:
        continue

    group = [e1]
    used[i] = True

    for j, e2 in enumerate(raw_ellipses):
        if used[j]:
            continue

        #merkezleri yakın ve boyutları benzr ise aynı halka olarak işaretler
        if abs(e1[0][0]-e2[0][0]) < 6 and abs(e1[0][1]-e2[0][1]) < 6 \
           and abs(e1[1][0]-e2[1][0]) < 20:
            group.append(e2)
            used[j] = True

    # bu iki halkaları ortalama alark tek olarak çiziyoruz resimde
    cx = int(np.mean([g[0][0] for g in group]))
    cy = int(np.mean([g[0][1] for g in group]))
    a  = int(np.mean([g[1][0] for g in group]))
    b  = int(np.mean([g[1][1] for g in group]))
    ang = int(np.mean([g[2] for g in group]))

    merged.append(((cx,cy),(a,b),ang))

ellipses = sorted(merged, key=lambda e: e[1][0]*e[1][1]) # halkaları kücükten büyüge icten dısa sıralarız

# eksik cıkanhalka icin ekstra gerekti baştan halka sayısını verdik
EXPECTED_RINGS = 10   # dart halka sayısı

if len(ellipses) == EXPECTED_RINGS - 1:  # 1 eksikse muhtemel en dıştır
    last = ellipses[-1]
    (cx,cy),(w,h),ang = last

    scale = 1.07 
    new_outer = ((cx,cy),(int(w*scale),int(h*scale)),ang) #son halkayı büyütür
    ellipses.append(new_outer)

# gri boyalı atışlar
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower_gray = np.array([0, 0, 60])
upper_gray = np.array([180, 60, 200])

gray_mask = cv2.inRange(hsv, lower_gray, upper_gray) # sadece dart izleri beyaz

# cv2.imshow("gray",gray_mask) # sınırlar çift çizgili, griler ve ufak lekeler beyaz diger yerler siyah

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
gray_mask = cv2.morphologyEx(gray_mask, cv2.MORPH_OPEN, kernel) # gürültü temizler
gray_mask = cv2.morphologyEx(gray_mask, cv2.MORPH_CLOSE, kernel)

cnts_pts, _ = cv2.findContours(
    gray_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
)

# elips mesafe, noktanın  elipsin neresinde oldugu
def elliptic_distance(x, y, ellipse):
    (cx, cy), (W, H), angle = ellipse
    a = W / 2
    b = H / 2
    t = np.deg2rad(angle)

    dx = x - cx
    dy = y - cy

    xr = dx*np.cos(t) + dy*np.sin(t)
    yr = -dx*np.sin(t) + dy*np.cos(t)

    return math.sqrt((xr/a)**2 + (yr/b)**2) #1 den büyükse dışında degilse icinde

# puan
ring_count = len(ellipses)
total_score = 0

for c in cnts_pts:
    area = cv2.contourArea(c)
    if area < 60 or area > 1500:
        continue

    M = cv2.moments(c)
    if M["m00"] == 0:
        continue

    px = int(M["m10"] / M["m00"])
    py = int(M["m01"] / M["m00"])

    # atışlar
    dists = [elliptic_distance(px, py, e) for e in ellipses] # her atış için tüm halkalara olan normalize mesafesi

    score = 0

    if dists[0] <= 1.0: #en iç halkaysa max puan
        score = ring_count 
    else:
        for i in range(len(dists)-1):
            if dists[i] > 1.0 and dists[i+1] <= 1.0:
                score = ring_count - (i+1) #hangi 2 halka arasındaysa
                break

    total_score += score

    cv2.drawContours(output, [c], -1, (0,0,255), 2) # gri bulunmuş alanları kırmızı ile ciziyor
    cv2.circle(output, (px,py), 3, (0,0,255), -1) # atışın tam koordinatını gösteriyor ufak bir yuvarlakla
    cv2.putText(output, str(score),(px+5, py-5),cv2.FONT_HERSHEY_SIMPLEX, 0.6,(0,0,255), 2) #atışın hemen yanına  hangi puana denk geldiğini yazar

for e in ellipses:
    cv2.ellipse(output, e, (255,0,0), 2) #mavi ile dart sınırları çizilir, koya aldığımız resim üzerine

cv2.putText(output, f"Toplam: {total_score}",(10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2) #kırmızı ile toplam puan

cv2.imshow("Dart Puan Hesaplama", output)
cv2.waitKey(0)
cv2.destroyAllWindows()