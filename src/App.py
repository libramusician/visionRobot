import asyncio

import cv2
from openni import openni2 as ni
import threading

import websockets

from boundingBox import BoundingBox
from detector.AutoDetector import AutoDetector
from src.receiver.CameraReceiver import CameraReceiver
from src.receiver.UDPReceiver import UDPReceiver
from src.detector.ManualDetector import ManualDetector
from Analyzer import analysis
from src.sender.UDPSender import UDPSender
from src.sender.WSSender import WSSender
from states.detecting import Detecting
from states.tracking import Tracking
from states.singleTracking import SingleTracking
from states.singleDetecting import SingleDetecting

# receiver = CameraReceiver()
ctraddr = ("127.0.0.1", 8002)
# frame_addr = ("192.168.137.24", 6000)
frame_addr = ("127.0.0.1", 6000)


class App:
    """
    fields:

    """
    def __init__(self):
        self.receiver = UDPReceiver()
        self.detector = AutoDetector()
        self.sender = UDPSender(ctraddr)

        self.trackers = []
        self.single_tracker = None
        self.mode_switch_counter = 0
        self.detecting = Detecting(self)
        self.tracking = Tracking(self)
        self.single_tracking = SingleTracking(self)
        self.single_detecting = SingleDetecting(self)
        self.current_state = self.detecting
        cv2.namedWindow("frame")
        self.mouse_position = None
        cv2.setMouseCallback("frame", self.mouse_clicked)

    def mouse_clicked(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print("mouse clicked")
            self.mouse_position = (x, y)
            print(self.mouse_position)
            self.current_state.mode_switch()

    def clean_up(self):
        cv2.destroyAllWindows()
        self.receiver.close()
        self.sender.close()

    def run(self):
        # ui_sender = WSSender()
        # threading.Thread(target=ui_sender.run, daemon=True).start()

        # send initial hello
        self.receiver.connect(frame_addr)
        print("waiting for first frame...")
        # frame = self.receiver.receive()
        # print("received first frame")

        # bbox: BoundingBox = self.detector.detect(frame)
        # tracker.init(self.receiver.current_frame, (bbox.get_xywh()))
        # cv2.destroyAllWindows()
        # print("tracker ready")
        # # the control code for first frame is useless, so send no operation
        # self.sender.send("0")

        while True:
            frame = self.receiver.receive()
            self.current_state.receive(frame)
            # ok, bbox_n = tracker.update(frame)
            # if ok:
            #     bbox.relocate(bbox_n)
            #     bbox.draw_on(frame)
            #
            #     region = analysis(bbox)
            # else:
            #     region = "0"
            # print("send region")

            if self.current_state is not self.single_tracking:
                self.sender.send("0")

            ok, frame_bytes = cv2.imencode(".jpg", frame)
            frame_str = frame_bytes.tobytes()
            # asyncio.run(ui_sender.send(frame_str))

            cv2.imshow("frame", frame)
            if cv2.waitKey(16) == ord('q'):
                break
        self.clean_up()


if __name__ == "__main__":
    a = App()
    a.run()
