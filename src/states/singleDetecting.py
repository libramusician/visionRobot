from states.serverState import ServerState
from boundingBox import draw
from boundingBox import BoundingBox
from states.tracking import distance_between_2points
from boundingBox import iou
import tracker_ex


class SingleDetecting(ServerState):
    def mode_switch(self):
        pass

    def receive(self, frame):
        detector = self.model.detector
        bboxes = detector.detect(frame)
        tracker = self.model.single_tracker
        if len(bboxes) == 0:
            # detect fail but tracker still work, back to tracking
            if tracker.ok:
                self.model.current_state = self.model.single_tracking
                print("enter single tracking")
                return
            # both fail, continue detect
            else:
                return
        # detection success, update targets
        else:
            bbox: BoundingBox
            box_in_tracker = BoundingBox(tracker.bbox)
            boxes_iou = {}
            for bbox in bboxes:
                box_iou = iou(box_in_tracker, bbox)
                boxes_iou[box_iou] = bbox
            closest = max(boxes_iou)
            if closest > 0.3:
                best_box = boxes_iou[closest]
                new_tracker = tracker_ex.Tracker()
                new_tracker.init(frame, best_box.get_xywh())
                self.model.single_tracker = new_tracker
                draw(best_box.get_xywh(), frame)
            self.model.current_state = self.model.single_tracking

