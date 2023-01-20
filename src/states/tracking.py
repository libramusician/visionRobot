import cv2

from states.serverState import ServerState
from boundingBox import draw
import boundingBox


def distance_between_2points(p1, p2):
    """
    sqrt((x1-x2)^2+(y1-y2)^2)
    :param p1:
    :param p2:
    :return:
    """
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


class Tracking(ServerState):

    def mode_switch(self):
        position = self.model.mouse_position
        trackers = self.model.trackers
        distance_tracker_position = {}
        for tracker in trackers:
            bbox = boundingBox.BoundingBox(tracker.bbox)
            distance = distance_between_2points(bbox.get_center(), position)
            distance_tracker_position[distance] = tracker
        closest = min(distance_tracker_position)
        best_tracker = distance_tracker_position[closest]
        self.model.single_tracker = best_tracker
        self.model.current_state = self.model.single_tracking

    def receive(self, frame):
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
        # print(counter)

        if counter == 0:
            self.model.current_state = self.model.detecting
            print("enter detecting")
