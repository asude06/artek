import cv2

def resizewithAspectRatio(img, width= None, height= None, inter = cv2.INTER_AREA): # bpyutlandırma çakışma olmasın diye varsayılan

    dimension = None
    (h,w) = img.shape[:2]

    if width is None and height is None:
        return img

# en vermediyse boydan oranla, boy vermediyse enden oranla

    if width is None:
        r = height / float(h)
        dimension = (int(w*r),height)

    else:
        r = width / float(w)
        dimension = (width, int(h*r))

    return cv2.resize(img, dimension, interpolation= inter)

img = cv2.imread("smile.jpg")
img1 = resizewithAspectRatio(img, width= None, height= 600, inter = cv2.INTER_AREA)

cv2.imshow("orijinal",img)
cv2.imshow("resized",img1)

cv2.waitKey((0))
cv2.destroyAllWindows()