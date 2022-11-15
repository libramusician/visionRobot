import asyncio

import numpy
import websockets
import base64

import cv2

from src.receiver.CameraReceiver import CameraReceiver
camera = CameraReceiver()

async def handler(websocket, path):
    # data = await websocket.recv()
    while True:
        frame:numpy.ndarray = camera.receive()
        frame2:numpy.ndarray = cv2.resize(frame, (320,240))
        ok, frame_bytes = cv2.imencode(".jpg", frame2)
        # frame_str = base64.b64encode(frame_bytes.tobytes())
        frame_str:numpy.ndarray = frame_bytes.tobytes()
        print(frame_str)
        # msg = "dcode"
        #
        # bmsg = base64.b64encode(msg.encode())
        # print(bmsg)

        await websocket.send(frame_str)





# class UDPsource():
#     def __init__(self, upper_receiver:CameraReceiver):
#         self.receiver = upper_receiver
#         self.ip = "127.0.0.1"
#         self.send_port = 5000
#         self.receive_port = 5001
#         self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         self.s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         self.s2.bind((self.ip, self.receive_port))

    # def run(self):
    #     while True:
    #         frame = self.receiver.receive()
    #         frame2 = cv2.resize(frame, (320,240))
    #         ok, frame_bytes = cv2.imencode(".jpg", frame2)
    #         print(len(frame_bytes))
    #         self.s.sendto(frame_bytes, (self.ip, self.send_port))
    #         print("msg sent")
    #         response, addr = self.s2.recvfrom(4)
    #         print("msg recv")
    #         print(response)

if __name__=='__main__':
    start_server = websockets.serve(handler, "127.0.0.1", 8000)

    asyncio.get_event_loop().run_until_complete(start_server)

    asyncio.get_event_loop().run_forever()
