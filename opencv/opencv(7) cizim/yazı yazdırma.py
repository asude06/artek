import cv2
import numpy as np

canvas = np.zeros((1000,1000,3),dtype=np.uint8) + 255

font1 = cv2.FONT_HERSHEY_SIMPLEX
font2 = cv2.FONT_HERSHEY_COMPLEX
font3 = cv2.FONT_HERSHEY_SCRIPT_COMPLEX

cv2.putText(canvas, "OpenCV", (30, 200), font3, 5, (80,100,100), cv2.LINE_AA)
cv2.putText(canvas, "image", (30,100), font3, 5, (55,160,160), cv2.LINE_AA )

cv2.imshow("Canvas",canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()

