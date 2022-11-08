import socket

import cv2

from src.receiver.CameraReceiver import CameraReceiver


class UDPsource():
    def __init__(self, upper_receiver:CameraReceiver):
        self.receiver = upper_receiver
        self.ip = "127.0.0.1"
        self.send_port = 5000
        self.receive_port = 5001
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s2.bind((self.ip, self.receive_port))

    def run(self):
        while True:
            frame = self.receiver.receive()
            frame2 = cv2.resize(frame, (320,240))
            ok, frame_bytes = cv2.imencode(".jpg", frame2)
            print(len(frame_bytes))
            self.s.sendto(frame_bytes, (self.ip, self.send_port))
            print("msg sent")
            response, addr = self.s2.recvfrom(4)
            print("msg recv")
            print(response)

if __name__=='__main__':
    r = UDPsource(CameraReceiver())
    r.run()