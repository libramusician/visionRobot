import cv2

from states.serverState import ServerState
from boundingBox import draw


class Tracking(ServerState):
    def receive(self, frame):
        tracker: cv2.TrackerKCF
        for tracker in self.model.trackers:
            ok, bbox = tracker.update(frame)
            if not ok:
                self.model.trackers.remove(tracker)
                print("target lost")
            else:
                draw(bbox, frame)
        # TODO: counter to detection
