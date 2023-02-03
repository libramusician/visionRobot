from states.serverState import ServerState
from boundingBox import draw
from analyzer.Analyzer import analysis
import boundingBox


class SingleTracking(ServerState):
    def mode_switch(self):
        pass

    def receive(self, frame):
        tracker = self.model.single_tracker
        ok, bbox = tracker.update(frame)
        if not ok:
            print("target lost")
            self.model.current_state = self.model.single_detecting
            print("enter detecting")
        draw(bbox, frame)
        region = analysis(boundingBox.BoundingBox(bbox))
        self.model.sender.send(region)

        self.model.mode_switch_counter = (self.model.mode_switch_counter + 1) % 10
        counter = self.model.mode_switch_counter
        print(counter)
        if counter == 0:
            self.model.current_state = self.model.single_detecting
            print("enter detecting")
