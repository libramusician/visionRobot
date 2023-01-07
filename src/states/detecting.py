import cv2

from states.serverState import ServerState
from boundingBox import BoundingBox, draw


class Detecting(ServerState):
    def receive(self, frame):
        bboxes = self.model.detector.detect(frame)
        # detection failed
        if len(bboxes) == 0:
            # nothing tracked, continue detection in the next frame
            if len(self.model.trackers) == 0:
                return
            # tracking may still work, continue tracking in the next frame
            else:
                self.model.current_state = self.model.tracking
        # detection success, update targets
        else:
            bbox: BoundingBox
            for bbox in bboxes:
                draw(bbox.get_xywh(), frame)
                # check if this target was being tracked
                tracker = bbox.is_tracked_by(self.model.trackers, frame)
                # found target also being tracked, update bounding box
                if tracker is not None:
                    tracker.init(frame, (bbox.get_xywh()))

                # target not being tracked, create a tracker to track it
                else:
                    tracker: cv2.TrackerKCF = cv2.TrackerKCF_create()
                    tracker.init(frame, (bbox.get_xywh()))
                    self.model.trackers.append(tracker)
                    # self.targets.append(bbox)
            # finish updating, back to track
            self.model.current_state = self.model.tracking

    def enter(self):
        pass
