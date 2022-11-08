import socket


class UDPSender():
    def __init__(self):
        ip = "127.0.0.1"
        send_port = 5001
        self.addr = (ip,send_port)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, response:int):
        self.s.sendto(response.to_bytes(4,'big', signed=True), self.addr)