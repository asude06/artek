"""
abs yöntemi 2 frame/goruntu arasında piksel bazlı mutlak farkı hesaplıyormuş
hareket tespiti, degisim algılama, arka plan cıkarma

ayni pikseler pikseller siyah 0, farkli pikseller beyaz görünür (yani sadece degisen bolgeler gozukur)

absdiff sonucu gürültülü olurmuş sonrasında threshold yapmak gerekir
kontur ile olay algilama

atis oncesi ve sonrasi gorüntüleri yükleriz ona gore farkı yakalar
(onceki durumda olmayan her seyi bul islemi yapacagiz)
"""
import cv2
import numpy as np
import math

ref = cv2.imread("dart1.jpeg")
img = cv2.imread("dart5.jpeg")

if ref is None or img is None:
    raise Exception("resimler yuklenemedi")

out = img.copy()

# yogunluk farkı icin gerekli
ref_gray = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(img_gray, 50, 150) #sınırlar belirlenir

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)


cnts, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
ellipses = []

for c in cnts:
    if len(c) < 100:
        continue
    if cv2.contourArea(c) < 2000:
        continue
    ellipses.append(cv2.fitEllipse(c)) #halk aelips ile modellenir

merged = []
used = [False]*len(ellipses)

for i, e1 in enumerate(ellipses):
    if used[i]:
        continue

    group = [e1]
    used[i] = True

    for j, e2 in enumerate(ellipses):
        if used[j]:
            continue

        if abs(e1[0][0]-e2[0][0]) < 6 and \
           abs(e1[0][1]-e2[0][1]) < 6 and \
           abs(e1[1][0]-e2[1][0]) < 20:
            group.append(e2)
            used[j] = True 
            
    #aynı merkeze ve benzer boyuta sahip elipsler aynı kabul edilir

    cx = int(np.mean([g[0][0] for g in group]))
    cy = int(np.mean([g[0][1] for g in group]))
    w  = int(np.mean([g[1][0] for g in group]))
    h  = int(np.mean([g[1][1] for g in group]))
    ang = int(np.mean([g[2] for g in group]))

    merged.append(((cx,cy),(w,h),ang)) #tek elips uretir

# içten dışa sırala
ellipses = sorted(merged, key=lambda e: e[1][0]*e[1][1])

#oncekinde olmayanlar beyaz
diff = cv2.absdiff(ref_gray, img_gray)
_,diff_bin = cv2.threshold(diff, 25,255,cv2.THRESH_BINARY)

# gürültü temizleme bosluk doldurma
diff_bin = cv2.morphologyEx(diff_bin, cv2.MORPH_OPEN, kernel)
diff_bin = cv2.morphologyEx(diff_bin, cv2.MORPH_CLOSE, kernel)

cnts_pts,_ = cv2.findContours(diff_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

def ellitic_distance(x, y, ellipse): #nktanın nerde oldugunu hesapalar halkaya gore
    (cx, cy), (W,H), ang = ellipse
    a, b = W/2, H/2
    t = np.deg2rad(ang)

    dx, dy = x-cx, y-cy
    xr = dx*np.cos(t) + dy*np.sin(t)
    yr = -dx*np.sin(t) + dy*np.cos(t)

    return math.sqrt((xr/a)**2 + (yr/b)**2)

ring_count = len(ellipses)
total_score = 0

for c in cnts_pts:
    if cv2.contourArea(c) < 50:
        continue
    
    M = cv2.moments(c)
    if M["m00"] == 0:
        continue

    px = int(M["m10"]/M["m00"])
    py = int(M["m01"]/M["m00"])

    dists = [ellitic_distance(px,py,e) for e in ellipses]

    score = 0
    for i in range(len(dists)):
        if dists[i] <= 1.0: #halka ici
            score = i+1  #1 den 5 e dogru
            break

    total_score += score

    cv2.circle(out, (px,py), 4, (0,0,255), -1)
    cv2.putText(out, str(score), (px+6, py-6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255),2)

for e in ellipses:
    cv2.ellipse(out, e, (255,0,0), 2)

cv2.putText(out, f"Toplam: {total_score}", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

cv2.imshow("Dart_Puan_Hesaplama - AbsDiff", out)
cv2.waitKey(0)
cv2.destroyAllWindows()