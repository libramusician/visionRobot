import asyncio
import time

import websockets

ip = "127.0.0.1"

port = 8000


class WSSender:
    def __init__(self):
        self.observers = set()
        self.frame = None

    async def handler(self, link):
        print(type(link))
        self.observers.add(link)
        while True:
            data = await link.recv()
            print(data)
            # for item in self.observers:
            #     await item.send(self.frame)

    async def send(self, message):
        for item in self.observers:
            await item.send(message)

    async def temp(self):
        async with websockets.serve(self.handler, ip, port):
            await asyncio.Future()

    def run(self):
        # time.sleep(1000)
        asyncio.run(self.temp())
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        # loop.run_until_complete(start_server)
        # loop.run_forever()


if __name__ == "__main__":
    WSSender().run()
