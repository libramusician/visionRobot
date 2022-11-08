import cv2
import numpy

GREEN = (0, 255, 0)
THICKNESS = 2


class BoundingBox:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.color = GREEN
        self.thickness = THICKNESS

    def relocate(self, bbox):
        self.x = int(bbox[0])
        self.y = int(bbox[1])
        self.w = int(bbox[2])
        self.h = int(bbox[3])

    def get_center(self):
        return (self.x + self.w / 2), (self.y + self.h / 2)

    def draw_on(self, frame: numpy.ndarray):
        cv2.rectangle(frame, (self.x, self.y), (self.x + self.w, self.y + self.h), self.color, thickness=self.thickness)

    def get_xywh(self):
        return self.x, self.y, self.w, self.h
