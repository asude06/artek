#kurulumu yap bu bilgisayarda path ayarla sonrasında resimdeki metini okutuyor

from PIL import Image
import pytesseract

img = Image.open("C:\\Users\\Asus\\Desktop\\artek\\3.1 text.png.png")
text = pytesseract.image_to_string(img,lang="eng")
print(text)

