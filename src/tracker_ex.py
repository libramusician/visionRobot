import cv2
import boundingBox


class Tracker:
    """
    bbox: bounding box in (x, y, w, h)
    """
    def __init__(self):
        self.tracker: cv2.TrackerKCF = cv2.TrackerKCF.create()
        self.bbox = None
        self.frame = None
        self.ok = False

    def init(self, img, bbox):
        self.tracker.init(img, bbox)
        self.frame = img
        self.bbox = bbox

    def update(self, img):
        ok, bbox = self.tracker.update(img)
        self.frame = img
        self.bbox = bbox
        self.ok = ok
        return ok, bbox

    def get_img_in_box(self):
        (x, y, w, h) = self.bbox
        roi = self.frame[x:x+w][y:y+w]
        cv2.imshow("roi", roi)
        return roi
