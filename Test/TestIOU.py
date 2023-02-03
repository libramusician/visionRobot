import cv2.xfeatures2d

from src.boundingBox import *
import unittest


class TestIOU(unittest.TestCase):
    def testIOU(self):
        box1 = BoundingBox((1, 2, 30, 40))
        box2 = BoundingBox((3, 4, 30, 40))

        self.assertTrue(iou(box1, box2) - 0.7964 < 0.001)

cv2.xfeatures2d.SIFT_create()
