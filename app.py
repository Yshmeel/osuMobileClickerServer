import sys
from config import config
import argparse
import socket
from pynput.keyboard import Controller 
import asyncio
import websockets
import json, time

"""
    osu! mobile clicker
    transforms your smartphone into keyboard clicker
    :author Yshmeel
"""

keyboard_controller = Controller() 

# https://stackoverflow.com/a/1267524
listen_port = 3125

parser = argparse.ArgumentParser(description='Setting up socket-server')
parser.add_argument("--ip", type=str, help="ip to listen")
parser.add_argument("--port", type=str, help="port to listen")

args = parser.parse_args()
if args.ip != None:
    listen_ip = args.ip
else:
	listen_ip = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
if args.port != None:
    listen_port = args.port

connected = []

async def listen(websocket, path):
    ip = websocket.remote_address[0]
    
    if ip not in connected:
        connected.append(ip)
        print(f"- A new client connected. IP: {ip}")
    
    try:
        async for message in websocket:
            message_object = json.loads(message)
            event = message_object['event']
            if event == "key_press_1":
                keyboard_controller.press(config['key_1'])
            if event == "key_press_2":
                keyboard_controller.press(config['key_2'])
            if event == "key_release_1":
                keyboard_controller.release(config['key_1'])
            if event == "key_release_2":
                keyboard_controller.release(config['key_2'])
    except OSError:
        raise
    finally:
        if ip in connected:
            connected.remove(ip)
        print(f"- Client disconnected. IP: {ip}")


print("osu! mobile clicker")

try:
    start_server = websockets.serve(listen, listen_ip, listen_port, max_queue=99999, read_limit=99999, write_limit=99999, ping_interval=0.01)

    asyncio.get_event_loop().run_until_complete(start_server)
    print("- Listening at " + "{ip}:{port}".format(ip=listen_ip, port=listen_port))
    asyncio.get_event_loop().run_forever()
except OSError:
    print(f"# Unfortunately, a server can't bind to {listen_ip} server, maybe try another ip or port? See `python app.py -h` to help")
