import cv2


cap = cv2.VideoCapture("C:\\Users\\Asus\\Desktop\\cicekli.mp4")

while True:
    ret, frame = cap.read()

    if ret == 0:
        break

    cv2.imshow("video",frame)

    if cv2.waitKey(10) & 0xFF == ord("a"):

        cv2.namedWindow("an")

        cv2.imwrite("../opencv/opencv(6) görsel/an.jpg", frame)
        cv2.imshow("an.jpg",frame)

        cv2.destroyAllWindows()



cap.release()
cv2.destroyAllWindows()


