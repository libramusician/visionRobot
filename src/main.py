import cv2 as cv
import numpy as np

face_cascade = cv.CascadeClassifier("haarcascade_frontalface_default.xml")
buffer = np.zeros((10,4), int)

def object_detect(img, cascade):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    objs = cascade.detectMultiScale(gray, 1.7)
    for (x, y, w, h) in objs:
        cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        object_detect(frame, face_cascade)

        cv.imshow("frame",frame)

        if cv.waitKey(16) == ord('q'):
            break
    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()
