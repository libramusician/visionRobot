import cv2.aruco
import numpy

import fps
from receiver.CameraReceiver import CameraReceiver
from boundingBox import draw

dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)


def generate_marker():
    # 200 x 200, 0 - 255
    maker_buffer = numpy.zeros((200, 200), dtype=numpy.uint8)
    marker = cv2.aruco.drawMarker(dictionary, 0, 200, img=maker_buffer, borderBits=1)
    cv2.imwrite("marker.png", marker)


def marker_detect():
    receiver = CameraReceiver()
    tracker: cv2.TrackerKCF
    counter = 0
    need_init = True
    while True:
        frame = receiver.receive()
        process_frame(frame, counter, need_init, tracker)

        cv2.imshow("f", frame)
        cv2.waitKey(10)


@fps.add_fps
def process_frame(frame, counter, need_init, tracker):
    # parameters = cv2.aruco.DetectorParameters_create()
    marker_corners, _, _ = cv2.aruco.detectMarkers(frame, dictionary)
    if counter != 0:
        if not need_init:
            ok, bbox = tracker.update(frame)
            if not ok:
                need_init = True

            else:
                draw(bbox, frame)
    else:
        if len(marker_corners) > 0:
            x1 = int(marker_corners[0][0][0][0])
            y1 = int(marker_corners[0][0][0][1])
            x2 = int(marker_corners[0][0][2][0])
            y2 = int(marker_corners[0][0][2][1])
            # cv2.rectangle(frame,
            #               (x1, y1),
            #               (x2, y2),
            #               (255, 0, 0), thickness=2)
            tracker: cv2.TrackerKCF = cv2.TrackerKCF.create()
            tracker.init(frame, (x1, y1, (x2 - x1), (y2 - y1)))
            need_init = False
    counter = (counter + 1) % 10


@fps.add_fps
def foo(frame):
    pass


# generate_marker()
marker_detect()
