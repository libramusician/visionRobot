import cv2
import numpy


class CameraReceiver():
    def __init__(self):
        self.source = cv2.VideoCapture(0)
        self.current_frame = None
        self.source.set(3, 320)
        self.source.set(4, 240)

    def receive(self) -> numpy.ndarray:
        ok, self.current_frame = self.source.read()
        if not ok:
            raise IOError("camera not opened")
        return self.current_frame
