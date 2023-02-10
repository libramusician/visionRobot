import asyncio
import time

import websockets

ip = "127.0.0.1"

port = 50000


class WSSender:
    def __init__(self):
        self.observers = set()
        self.frame = None

    async def handler(self, link):
        print(type(link))
        self.observers.add(link)
        while True:
            try:
                data = await link.recv()
                print(data)
            except websockets.ConnectionClosed:
                print("connection closed")
                self.observers.remove(link)
                break

    async def send(self, message):
        for item in self.observers:
            await item.send(message)

    async def temp(self):
        async with websockets.serve(self.handler, ip, port):
            await asyncio.Future()

    def run(self):
        asyncio.run(self.temp())



if __name__ == "__main__":
    WSSender().run()
