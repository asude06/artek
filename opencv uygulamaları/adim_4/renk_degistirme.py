import numpy as np
import argparse
import cv2

def image_stats(image):
    # her kanal için ortalama ve standart sapma hesaplaması yapılır
    (l, a, b) = cv2.split(image)

    (lMean, lStd) = (l.mean(), l.std())
    (aMean, aStd) = (a.mean(), a.std())
    (bMean, bStd) = (b.mean(), b.std())

    return (lMean, lStd, aMean, aStd, bMean, bStd)


def color_transfer(source, target):
    # BGR → LAB dönüşümü (float32 zorunlu)
    source = cv2.cvtColor(source, cv2.COLOR_BGR2LAB).astype("float32")
    target = cv2.cvtColor(target, cv2.COLOR_BGR2LAB).astype("float32")

    # renk istatistiklerini hesaplanır
    (lMeanSrc, lStdSrc, aMeanSrc, aStdSrc, bMeanSrc, bStdSrc) = image_stats(source)
    (lMeanTar, lStdTar, aMeanTar, aStdTar, bMeanTar, bStdTar) = image_stats(target)

    # hedef görüntünün kanallarını ayır
    (l, a, b) = cv2.split(target)

    # ortalamaları çıkar
    l -= lMeanTar
    a -= aMeanTar
    b -= bMeanTar

    # standart sapmaya göre ölçekle
    l = (lStdSrc / lStdTar) * l
    a = (aStdSrc / aStdTar) * a
    b = (bStdSrc / bStdTar) * b

    # kaynak ortalamalarını ekle
    l += lMeanSrc
    a += aMeanSrc
    b += bMeanSrc

    # [0,255] aralığına kırp
    l = np.clip(l, 0, 255)
    a = np.clip(a, 0, 255)
    b = np.clip(b, 0, 255)

    # kanalları birleştir ve BGR'ye geri dön
    transfer = cv2.merge([l, a, b])
    transfer = cv2.cvtColor(transfer.astype("uint8"), cv2.COLOR_LAB2BGR)

    return transfer

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--source", required=True, help="kaynak görüntü yolu")
ap.add_argument("-t", "--target", required=True, help="hedef görüntü yolu")
ap.add_argument("-o", "--output", required=True, help="çıktı görüntü yolu")
args = vars(ap.parse_args())

source = cv2.imread(args["source"])
target = cv2.imread(args["target"])

if source is None or target is None:
    raise IOError("Görüntüler okunamadı. Dosya yollarını kontrol et.")

# renk aktarımı yap
result = color_transfer(source, target)

# sonucu kaydet ve göster
cv2.imwrite(args["output"], result)

cv2.imshow("Source", source)
cv2.imshow("Target", target)
cv2.imshow("Color Transfer Result", result)
cv2.waitKey(0)
cv2.destroyAllWindows()

# python renk_degistirme.py -s source.jpg -t target.jpg -o result.jpg