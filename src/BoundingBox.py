import cv2
import numpy

GREEN = (0, 255, 0)
THICKNESS = 2
IOU_THRESHOLD = 0.5


def draw(bbox, frame: numpy.ndarray):
    x = bbox[0]
    y = bbox[1]
    w = bbox[2]
    h = bbox[3]
    cv2.rectangle(frame, (x, y), (x + w, y + h), GREEN, thickness=THICKNESS)


class BoundingBox:
    def __init__(self, bbox):
        self.x = bbox[0]
        self.y = bbox[1]
        self.w = bbox[2]
        self.h = bbox[3]
        self.color = GREEN
        self.thickness = THICKNESS

    def get_center(self):
        return (self.x + self.w / 2), (self.y + self.h / 2)

    # def draw_on(self, frame: numpy.ndarray):
    #     cv2.rectangle(frame, (self.x, self.y), (self.x + self.w, self.y + self.h), self.color, thickness=self.thickness)

    def get_xywh(self):
        return self.x, self.y, self.w, self.h

    def set_xywh(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def is_tracked_by(self, trackers, frame):
        confidences = {}
        tracker: cv2.TrackerKCF
        print(trackers)
        for tracker in trackers:
            ok, bbox = tracker.update(frame)
            iou_ratio = iou(self, BoundingBox(bbox))
            confidences[iou_ratio] = tracker
            # TODO: simple, use max to be more accurate
        if len(confidences) == 0:
            return None
        else:
            best = max(confidences)
            if best > IOU_THRESHOLD:
                return confidences[best]
            else:
                return None


def iou(a: BoundingBox, b: BoundingBox):
    area_a = a.w * a.h
    area_b = b.w * b.h
    w = min(b.x + b.w, a.x + a.w) - max(a.x, b.x)
    h = min(b.y + b.h, a.y + a.h) - max(a.y, b.y)
    if w <= 0 or h <= 0:
        return 0
    area_c = w * h
    return area_c / (area_a + area_b - area_c)
