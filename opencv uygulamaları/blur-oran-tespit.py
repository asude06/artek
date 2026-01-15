import cv2

IMAGE_PATH = "blur-resim.jpg"  
THRESHOLD = 100.0          # bulanıklık eşiği

def variance_of_laplacian(image): #ani yogunluk degisimlerini bulur, ikinci turev alıyormus
    """Görüntü netlik ölçüsü"""
    return cv2.Laplacian(image, cv2.CV_64F).var() # varyans net goruntu yuksek varyans, bulanık goruntu dusuk varyans

image = cv2.imread(IMAGE_PATH)

if image is None:
    print("Görüntü yüklenemedi. Yol yanlış olabilir.")
    exit()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
fm = variance_of_laplacian(gray)

label = "Not Blurry"
if fm < THRESHOLD: # esik degere gore kıyaslıyoruz
    label = "Blurry"

cv2.putText(
    image,
    f"{label}: {fm:.2f}",
    (10, 30),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.8,
    (0, 0, 255), #kırmızı
    2
)

print(f"Blur Score: {fm:.2f} -> {label}")

cv2.imshow("Blur Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()