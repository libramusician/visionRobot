import cv2

# from detector.AutoDetector import AutoDetector
# from src.receiver.CameraReceiver import CameraReceiver
from src.receiver.UDPReceiver import UDPReceiver
# from src.detector.ManualDetector import ManualDetector
from analyzer.Analyzer import analysis
from src.sender.UDPSender import UDPSender
# from src.sender.WSSender import WSSender
# from states.detecting import Detecting
# from states.tracking import Tracking
# from states.singleTracking import SingleTracking
# from states.singleDetecting import SingleDetecting
import detector.markerDetector2 as markerDetector
import boundingBox

ctraddr = ("127.0.0.1", 8002)
#frame_addr = ("192.168.137.75", 6000)
frame_addr = ("127.0.0.1", 6000)


class App:
    """
    fields:

    """
    def __init__(self):
        self.receiver = UDPReceiver()
        self.sender = UDPSender(ctraddr)
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
            frame_str = frame_bytes.tobytes()
            # asyncio.run(ui_sender.send(frame_str))

            cv2.imshow("frame", frame)
            if cv2.waitKey(16) == ord('q'):
                break


if __name__ == "__main__":
    a = App()
    try:
        a.run()
    except KeyboardInterrupt:
        print("keyboard interrupt, execution finish")
    finally:
        a.clean_up()
