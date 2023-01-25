import socket

import cv2

from src.receiver.CameraReceiver import CameraReceiver


class UDPsource():
    def __init__(self, camera:CameraReceiver):
        self.receiver = camera
        self.ip = "127.0.0.1"
        self.send_port = 6000
        self.receive_port = 8002
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((self.ip, self.send_port))
        self.s2.bind((self.ip, self.receive_port))
        print("waiting for connection")
        # wait for hello message


    def run(self):
        data, addr = self.s.recvfrom(1024)
        print("connection received")
        while True:
            # grab frame from camera
            frame = self.receiver.receive()
            frame2 = cv2.resize(frame, (416, 416))
            ok, frame_bytes = cv2.imencode(".jpg", frame2)
            #print(len(frame_bytes))
            self.s.sendto(frame_bytes, addr)
            print("msg sent to " + str(addr))
            response, _ = self.s2.recvfrom(4)
            print("msg recv")
            print(response)

if __name__=='__main__':
    r = UDPsource(CameraReceiver())
    r.run()