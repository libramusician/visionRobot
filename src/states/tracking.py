import cv2

from states.serverState import ServerState
from boundingBox import draw


class Tracking(ServerState):
    def mode_switch(self, frame):
        pass

    def receive(self, frame):
        tracker: cv2.TrackerKCF
        for tracker in self.model.trackers:
            ok, bbox = tracker.update(frame)
            if not ok:
                print(self.model.trackers)
                print(tracker)
                self.model.trackers.remove(tracker)
                print(self.model.trackers)
                print("target lost")
                self.model.current_state = self.model.detecting
                print("enter detecting")
            else:
                draw(bbox, frame)
        # TODO: counter to detection
        self.model.mode_switch_counter = (self.model.mode_switch_counter + 1) % 10
        counter = self.model.mode_switch_counter
        print(counter)
        if counter == 0:
            self.model.current_state = self.model.detecting
            print("enter detecting")
