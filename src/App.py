import argparse
import asyncio
import threading
import base64

import cv2

# from detector.AutoDetector import AutoDetector
# from src.receiver.CameraReceiver import CameraReceiver
from receiver.UDPReceiver import UDPReceiver
# from src.detector.ManualDetector import ManualDetector
from analyzer.Analyzer import analysis
from sender.UDPSender import UDPSender
from sender.WSSender import WSSender
# from states.detecting import Detecting
# from states.tracking import Tracking
# from states.singleTracking import SingleTracking
# from states.singleDetecting import SingleDetecting
import detector.markerDetector2 as markerDetector
import boundingBox



class App:
    """
    fields:

    """
    def __init__(self, ip):
        self.ctraddr = (ip, 8002)
        self.frame_addr = (ip, 6000)
        self.receiver = UDPReceiver()
        self.sender = UDPSender(self.ctraddr)
        self.ui_sender = WSSender()
        # self.detector = AutoDetector()
        # self.trackers = []

        # states
        # self.single_tracker = None
        # self.mode_switch_counter = 0
        # self.detecting = Detecting(self)
        # self.tracking = Tracking(self)
        # self.single_tracking = SingleTracking(self)
        # self.single_detecting = SingleDetecting(self)
        # self.current_state = self.detecting
        # cv2.namedWindow("frame")
        # self.mouse_position = None
        # cv2.setMouseCallback("frame", self.mouse_clicked)

    # def mouse_clicked(self, event, x, y, flags, param):
    #     if event == cv2.EVENT_LBUTTONDOWN:
    #         print("mouse clicked")
    #         self.mouse_position = (x, y)
    #         print(self.mouse_position)
    #         self.current_state.mode_switch()

    def clean_up(self):
        cv2.destroyAllWindows()
        self.receiver.close()
        self.sender.close()

    async def run(self):
        #
        # threading.Thread(target=self.ui_sender.run, daemon=True).start()
        # loop = asyncio.get_event_loop()
        # asyncio.create_task(self.ui_sender.start_server())
        # send initial hello
        self.receiver.connect(self.frame_addr)
        print("waiting for first frame...")

        while True:
            frame = self.receiver.receive()
            # self.current_state.receive(frame)

            # if self.current_state is not self.single_tracking:
            #     self.sender.send("0")

            detected, result = markerDetector.detect(frame)
            if not detected:
                self.sender.send("0")
            else:
                print(result)
                cmd = analysis(result)
                self.sender.send(cmd)

            ok, frame_bytes = cv2.imencode(".jpg", frame)

            frame_str = base64.b64encode(frame_bytes.tobytes())

            await self.ui_sender.send(frame_str)

            cv2.imshow("frame", frame)
            if cv2.waitKey(16) == ord('q'):
                break

async def wrapper(a):
    run_task = asyncio.create_task(a.run())
    server_task = asyncio.create_task(a.ui_sender.start_server())
    await asyncio.gather(run_task, server_task)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-ip", default="127.0.0.1")
    args = parser.parse_args()
    a = App(args.ip)
    try:
        asyncio.run(wrapper(a))
    except KeyboardInterrupt:
        print("keyboard interrupt, execution finish")
    finally:
        a.clean_up()
