from imutils.perspective import four_point_transform
import imutils
import cv2

DIGITS_LOOKUP = { # 7 segmenti olusturur
    (1,1,1,0,1,1,1): 0,
    (0,0,1,0,0,1,0): 1,
    (1,0,1,1,1,1,0): 2,
    (1,0,1,1,0,1,1): 3,
    (0,1,1,1,0,1,0): 4,
    (1,1,0,1,0,1,1): 5,
    (1,1,0,1,1,1,1): 6,
    (1,0,1,0,0,1,0): 7,
    (1,1,1,1,1,1,1): 8,
    (1,1,1,1,0,1,1): 9
}

image = cv2.imread("digit.webp")
image = imutils.resize(image, height=500) #ölçek sabitleme
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5,5), 0) #gürültü 
edged = cv2.Canny(blur, 50, 200) #kenar bulur

#en buyuk kenarları bulur 4 köşeli alanı lcd olarak kabul eder
cnts = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

for c in cnts:
    peri = cv2.arcLength(c, True) # oklşd uzakligi
    approx = cv2.approxPolyDP(c, 0.015 * peri, True)  #perspektif düzenleme
    if len(approx) == 4:
        displayCnt = approx
        break

warped_gray = four_point_transform(gray, displayCnt.reshape(4,2))
output = four_point_transform(image, displayCnt.reshape(4,2))

thresh = cv2.threshold( #lcd beyaz arka plan siyah
    warped_gray, 0, 255,
    cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
)[1]

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2)) # kucuk maske
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1) #dilatioon kucuk boslular ortulur, erosion ile gerçek sınırlar koruynur

cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # sadece dış konturları al
cnts = imutils.grab_contours(cnts)

digitCnts = []
decimalCnts = []

for c in cnts:
    x, y, w, h = cv2.boundingRect(c) #nokra ve konturları ayırt etmek

    # decimal
    if w < 12 and h < 12:
        decimalCnts.append((x, y, w, h))
        continue

    # rakam
    if h >= 30 and w >= 12:
        # birleşik rakam kontrolü 
        if w > 1.2 * h:
            digitCnts.append((x, y, w//2, h))
            digitCnts.append((x + w//2, y, w//2, h))
        else:
            digitCnts.append((x, y, w, h))

digitCnts = sorted(digitCnts, key=lambda b: b[0]) #soldan saga sıralar

digits = []

for (x, y, w, h) in digitCnts:
    roi = thresh[y:y+h, x:x+w] #görselde sadece o bölgenin işlem görmeis

    roiH, roiW = roi.shape #yukseklik ve genislik 
    dW = int(roiW * 0.28) #yatay segment genisligi
    dH = int(roiH * 0.18) # yatay segment yuk
    dHC = int(roiH * 0.08) # orta segment kalınlıgı

    segments = [
        ((dW, 0), (roiW-dW, dH)), # ust
        ((0, dH), (dW, roiH//2)), # sol ust
        ((roiW-dW, dH), (roiW, roiH//2)), # sag ust
        ((dW, roiH//2-dHC), (roiW-dW, roiH//2+dHC)), # orta
        ((0, roiH//2), (dW, roiH-dH)), # sol alt
        ((roiW-dW, roiH//2), (roiW, roiH-dH)), # sag alt
        ((dW, roiH-dH), (roiW-dW, roiH)) # alt
    ]

    on = [0]*7 #baslangıcta
    for i, ((xA,yA),(xB,yB)) in enumerate(segments):
        segROI = roi[yA:yB, xA:xB]
        area = (xB-xA)*(yB-yA)
        if area > 0 and cv2.countNonZero(segROI)/float(area) > 0.35: #beyaz oranını hesapla saglıyorsa yanıyor demektir
            on[i] = 1

    digit = DIGITS_LOOKUP.get(tuple(on)) #7-segment alfabesi
    if digit is not None: #rakam tanınıyorsa
        cx = x + w//2
        digits.append((digit, cx)) #kaydeder
        cv2.rectangle(output,(x,y),(x+w,y+h),(0,255,0),1) #rakamı yeşil kutu icine alır
        cv2.putText(output,str(digit),(x,y-10),
                    cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2) #tanınan rakamı yazar


#okunan degeri sadece rakam olarak degil ekranda ne yazıyorsa onun çıktısını dogru sekşlde alması icimn
result = ""

for i, (digit, cx) in enumerate(digits):
    result += str(digit)

    # son digitten sonra nokta YOK
    if i == len(digits) - 1:
        continue

    next_cx = digits[i+1][1]

    for dx, dy, dw, dh in decimalCnts:
        dcenter = dx + dw // 2
        if cx < dcenter < next_cx:
            result += "."
            break

print("Thermostat reading:", result, "°C")

cv2.imshow("Output", output)
cv2.imshow("Thresh", thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()