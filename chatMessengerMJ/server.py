#Good morning Jafar and/or the one and only Mr. Borat! this comment is just going to go over the setup of the ngrok IP port thingy, and how to do it since i'm currently probably meshing with my bed as we speak. before i begin describing, just know this was done on a windows pc using PowerShell, so if there are any issues try and see if it's because you guys are using a mac pc (i haven't tested mac and windows compatability). Without further ado, let me explain this thing.
#First, you must create your own ngrok account by going to their website and making one. Then find your authentication code, and copy it. Next, enter winget install ngrok.ngrok (or the alternative for the pc you're using). once that's done, you're gonna enter ngrok config add-authtoken (your_token) , and this should execute perfectly. Finally, you just need to type ngrok https 6767 . i just chose 6767 as the port because that's the first thing that came to mine, don't judge me bru. now a little menu should pop up with various sessionm status things on the left side. You're gonna find the Forwarding row, and copy all the text after https:// , however do not copy the space and arrow after it, nor the localhost thing that pops up. those are not important right now.
#The final step is to launch the server.py and the client.py (as many client.py s as you'd like, they should all be able to send messages to eachother. then enter wss://(paste the forwarding thing here, without the parentheses)/ws . Now, just enter a message and it should pop up in all of the clients. I am currently running on the fumes of fumes as of right now, so i'll try and explain how the layers are used in this pipeline.
# Layer 7 is the actual code in the two programs of server.py, and client.py . Layer 6 is the encryption of the data using the WSS encryption. Layer 5 is the handshake between the websockets, and keeping the server and clients running. Layer 4 is the use of TCP, as well as asyncio stopping blocking from happening in order to ensure that messages can be sent and received at the same time. Layer 3 does IP Routing, where the destination domain and Ip addresses are created, and breaks the TCP stream into IP packets for movement. Layer 2 packages Ip packets using MAC addresses to move data from machine to local router. and finally, layer 1, which translates the webSocket data into binary, and into radio waves or another kind of medium in order to move the data. That covers all the layers in this project, and how they're addressed!
#if prompted, install any neccessary libraries, and good luck! If i'm awake, i'll try and help Jafar with this.
#This code is intended to allow one computer to host 1 server, and have clients on any machine anywhere connect to that one computer's server. multiple clients as well as multiple servers should be able to exist at once.


import asyncio
import websockets
from websockets.asyncio.server import serve

message_list = set()
current_clients = {}
username_got=0

async def client_handler(websocket):
   raw_username = await websocket.recv()
   username = raw_username.strip()
   current_clients[websocket]=username
   print(f"New client: {username} websocket: {websocket}")
   message_list.add(websocket)
   while True:
      async for message in websocket:
         websockets.broadcast(message_list, f"{username}: {message}")

async def main():
   print("Server Setup")
   async with serve(client_handler, "0.0.0.0", 6767):
      await asyncio.Future()

if __name__ == "__main__":
   asyncio.run(main())

