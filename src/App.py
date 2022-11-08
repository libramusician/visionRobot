import cv2

from src import BoundingBox
from src.receiver.CameraReceiver import CameraReceiver
from src.receiver.UDPReceiver import UDPReceiver
from src.detector.ManualDetector import ManualDetector
from Analyzer import analysis
from src.sender.UDPSender import UDPSender

# receiver = CameraReceiver()
receiver = UDPReceiver()
detector = ManualDetector()
sender = UDPSender()
bbox:BoundingBox = detector.detect(receiver.receive())
tracker:cv2.TrackerKCF = cv2.TrackerKCF_create()
tracker.init(receiver.current_frame,(bbox.get_xywh()))
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
        print(region)
    else:
        print("target lost")
        region = -1
    sender.send(region)
    print("res sent")


    cv2.imshow("frame", frame)
    if cv2.waitKey(16) == ord('q'):
        break
cv2.destroyAllWindows()