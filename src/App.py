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


def run():
    print("1")
    ui_sender = WSSender()
    threading.Thread(target=ui_sender.run, daemon=True).start()
    receiver = UDPReceiver()
    detector = ManualDetector()
    sender = UDPSender()

    # uncomment to send initial hello
    #sender.send(1)

    bbox: BoundingBox = detector.detect(receiver.receive())
    tracker: cv2.TrackerKCF = cv2.TrackerKCF_create()
    tracker.init(receiver.current_frame, (bbox.get_xywh()))
    cv2.destroyAllWindows()
    print("tracker ready")
    sender.send(-1)
    while True:
        frame = receiver.receive()
        ok, bbox_n = tracker.update(frame)
        if ok:
            bbox.relocate(bbox_n)
            bbox.draw_on(frame)

            region = analysis(bbox)
        else:
            #print("target lost")
            region = -1
        sender.send(region)

        ok, frame_bytes = cv2.imencode(".jpg", frame)
        frame_str = frame_bytes.tobytes()
        asyncio.run(ui_sender.send(frame_str))

        cv2.imshow("frame", frame)
        if cv2.waitKey(16) == ord('q'):
            break
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run()
