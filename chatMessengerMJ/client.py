#this is simply the code for the client. install any neccessary libraries if you're prompted, and happy clienting bru!

import asyncio
import aioconsole
import websockets

async def send_a_message(websocket):
   print("Empty space is area in which you can type a message!")
   while True:
      await asyncio.sleep(0.2)
      message = await aioconsole.ainput("")   
      await websocket.send(message)
      print("sent!")

async def receive_a_message(websocket):
   while True:
      async for message in websocket:
         print(f"\n{message}")

async def main():
   uri = input("Please enter the uri of the server you'd like to connect to: ")
   async with websockets.connect(uri) as websocket:
      try:
         
         await websocket.send(input("Please enter your preferred username: "))
         await asyncio.gather(receive_a_message(websocket), send_a_message(websocket))
      except websockets.ConnectionClosed:
         print("Connection hath been closed")
   

if __name__ == "__main__":
   asyncio.run(main())
   
