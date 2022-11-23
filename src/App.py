import asyncio

import cv2
import threading

import websockets

from src import BoundingBox
from src.receiver.CameraReceiver import CameraReceiver
from src.receiver.UDPReceiver import UDPReceiver
from src.detector.ManualDetector import ManualDetector
from Analyzer import analysis
from src.sender.UDPSender import UDPSender
from src.sender.WSSender import WSSender


# receiver = CameraReceiver()
ctraddr = ("127.0.0.1", 8002)
#frame_addr = ("192.168.137.24", 6000)
frame_addr = ("127.0.0.1", 6000)


def run():
    #ui_sender = WSSender()
    #threading.Thread(target=ui_sender.run, daemon=True).start()

    receiver = UDPReceiver()
    detector = ManualDetector()
    sender = UDPSender(ctraddr)

    # send initial hello
    receiver.connect(frame_addr)
    print("waiting for first frame...")
    frame = receiver.receive()
    print("received first frame")
    bbox: BoundingBox = detector.detect(frame)
    tracker: cv2.TrackerKCF = cv2.TrackerKCF_create()
    tracker.init(receiver.current_frame, (bbox.get_xywh()))
    cv2.destroyAllWindows()
    print("tracker ready")
    # the control code for first frame is useless, so send no operation
    sender.send("0")
    while True:
        frame = receiver.receive()
        print("received second frame")
        ok, bbox_n = tracker.update(frame)
        if ok:
            bbox.relocate(bbox_n)
            bbox.draw_on(frame)

            region = analysis(bbox)
        else:
            region = "0"
        print("send region")
        sender.send(region)


        ok, frame_bytes = cv2.imencode(".jpg", frame)
        frame_str = frame_bytes.tobytes()
        #asyncio.run(ui_sender.send(frame_str))

        cv2.imshow("frame", frame)
        if cv2.waitKey(16) == ord('q'):
            break
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run()
