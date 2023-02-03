import cv2
import numpy
from src.boundingBox import BoundingBox


class ManualDetector:
    def __init__(self):
        self.bbox = BoundingBox()

    def detect(self, frame: numpy.ndarray):
        bbox_n = cv2.selectROI("select", frame)
        self.bbox.relocate(bbox_n)
        return self.bbox
