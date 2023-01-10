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

# receiver = CameraReceiver()
ctraddr = ("127.0.0.1", 8002)
# frame_addr = ("192.168.137.24", 6000)
frame_addr = ("127.0.0.1", 6000)


class App:
    def __init__(self):
        self.receiver = UDPReceiver()
        self.detector = AutoDetector()
        self.sender = UDPSender(ctraddr)

        self.trackers = []
        self.mode_switch_counter = 0
        self.detecting = Detecting(self)
        self.tracking = Tracking(self)
        self.current_state = self.detecting

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
        # tracker: cv2.TrackerKCF = cv2.TrackerKCF_create()
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

            # TODO: temp always set return 0
            region = "0"
            self.sender.send(region)

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
