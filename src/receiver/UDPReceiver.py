import socket

import cv2
import numpy


class UDPReceiver():
    def __init__(self):
        ip = "127.0.0.1"
        receive_port = 5000
        self.s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.s.bind((ip,receive_port))
        self.current_frame = None
        print("UDP receiver ready")

    def receive(self) -> numpy.ndarray:
        try:
            data, address = self.s.recvfrom(1048576)
            # print("got data")
            frame_arr = numpy.array(bytearray(data))
            self.current_frame = cv2.imdecode(frame_arr, cv2.IMREAD_UNCHANGED)
            return self.current_frame
        except Exception as e:
            print(e)
            print("connection stopped")
            exit(1)