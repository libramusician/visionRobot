import cv2

from states.serverState import ServerState
from boundingBox import BoundingBox, draw
import tracker_ex


class Detecting(ServerState):
    def mode_switch(self):
        pass

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
                print("enter tracking")
        # detection success, update targets
        else:
            bbox: BoundingBox
            for bbox in bboxes:
                draw(bbox.get_xywh(), frame)
                # check if this target was being tracked
                tracker = bbox.is_tracked_by(self.model.trackers, frame)
                # found target also being tracked, update bounding box
                if tracker is not None:
                    self.model.trackers.remove(tracker)
                    new_tracker = tracker_ex.Tracker()
                    new_tracker.init(frame, (bbox.get_xywh()))
                    self.model.trackers.append(new_tracker)
                    print("tracker updated")
                    print(tracker)

                # target not being tracked, create a tracker to track it
                else:
                    tracker: tracker_ex.Tracker = tracker_ex.Tracker()
                    tracker.init(frame, (bbox.get_xywh()))
                    self.model.trackers.append(tracker)
                    print("tracker added")
                    print(tracker)
            self.model.current_state = self.model.tracking
            print("enter tracking")

    def enter(self):
        pass
