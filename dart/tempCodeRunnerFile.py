
import cv2
import numpy as np
import imutils
import math

# ======================================================
# 1) RESİM
# ======================================================
image = cv2.imread("dart5.jpeg")
if image is None:
    raise Exception("Resim yüklenemedi")

output = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# ======================================================
# 2) ELİPTİK HALKALAR (AYNI – DEĞİŞMEDİ)
# ======================================================
blur_rings = cv2.GaussianBlur(gray, (5,5), 0)

th_rings = cv2.adaptiveThreshold(
    blur_rings, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY_INV,
    31, 5
)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
th_rings = cv2.morphologyEx(th_rings, cv2.MORPH_CLOSE, kernel)

edges_rings = cv2.Canny(th_rings, 40, 120)

cnts_rings, _ = cv2.findContours(
    edges_rings, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
)

raw_ellipses = []

for c in cnts_rings:
    if len(c) < 80:
        continue
    area = cv2.contourArea(c)
    if area < 1000:
        continue
    peri = cv2.arcLength(c, True)
    if peri == 0:
        continue
    circularity = 4 * math.pi * area / (peri * peri)
    if circularity < 0.3:
        continue
    raw_ellipses.append(cv2.fitEllipse(c))

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
        if abs(e1[0][0]-e2[0][0]) < 5 and abs(e1[0][1]-e2[0][1]) < 5 \
           and abs(e1[1][0]-e2[1][0]) < 15:
            group.append(e2)
            used[j] = True

    cx = int(np.mean([g[0][0] for g in group]))
    cy = int(np.mean([g[0][1] for g in group]))
    a  = int(np.mean([g[1][0] for g in group]))
    b  = int(np.mean([g[1][1] for g in group]))
    ang = int(np.mean([g[2] for g in group]))

    merged.append(((cx,cy),(a,b),ang))

ellipses = sorted(merged, key=lambda e: e[1][0]*e[1][1])

# ======================================================
# 3) GRİ BOYALI ALANLAR (ARTIK LEKE DEĞİL)
# ======================================================
blur_pts = cv2.GaussianBlur(gray, (7,7), 0)

th_pts = cv2.adaptiveThreshold(
    blur_pts, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY_INV,
    31, 7
)

kernel_big = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
th_pts = cv2.morphologyEx(th_pts, cv2.MORPH_CLOSE, kernel_big)
th_pts = cv2.morphologyEx(th_pts, cv2.MORPH_OPEN, kernel_big)

cnts_pts, _ = cv2.findContours(
    th_pts, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
)

# ======================================================
# 4) ELİPTİK MESAFE
# ======================================================
def elliptic_distance(x, y, ellipse):
    (cx, cy), (W, H), angle = ellipse
    a = W / 2
    b = H / 2

    theta = np.deg2rad(angle)
    cos_t, sin_t = np.cos(theta), np.sin(theta)

    dx = x - cx
    dy = y - cy

    xr =  dx*cos_t + dy*sin_t
    yr = -dx*sin_t + dy*cos_t

    return math.sqrt((xr/a)**2 + (yr/b)**2)

# ======================================================
# 5) PUANLAMA (BOYALI ALAN = TEK ATIS)
# ======================================================
total_score = 0
ring_count = len(ellipses)

for c in cnts_pts:
    area = cv2.contourArea(c)

    # 🔴 LEKE FİLTRESİ (KRİTİK)
    if area < 200:        # <-- en önemli satır
        continue

    M = cv2.moments(c)
    if M["m00"] == 0:
        continue

    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])

    score = 0
    for i, e in enumerate(ellipses):
        if elliptic_distance(cx, cy, e) <= 1.0:
            score = ring_count - i
            break

    total_score += score

    cv2.drawContours(output, [c], -1, (0,0,255), 2)
    cv2.putText(output, str(score), (cx+5, cy-5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

# ======================================================
# 6) ÇİZİM
# ======================================================
for e in ellipses:
    cv2.ellipse(output, e, (255,0,0), 2)

cv2.putText(output, f"Toplam: {total_score}",
            (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

print("Toplam Puan:", total_score)

cv2.imshow("Eliptik Dart – Boyalı Alan Bazlı Puanlama", output)
cv2.waitKey(0)
cv2.destroyAllWindows()
