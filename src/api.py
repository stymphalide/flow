#!/usr/bin/env python3.5
import asyncio
import websockets
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
import src.controller as c



async def game(websocket, path):
    while True:
      data = await websocket.recv()
      print("< {}".format(data))
      msg = c.parser(data)
      await websocket.send(msg)
      print("> {}".format(msg))

start_server = websockets.serve(game, 'localhost', 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()