import pygame
import os
import random
import actr.rpc_interface
import asyncio
import threading
import json
#from run_experiment import socket
from actr.socket_manager import comet_socket, move_socket
import time
#loop = None


def start_async_loop():
    global loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_forever()

#asyncio_thread = threading.Thread(target=start_async_loop, daemon=True)
#asyncio_thread.start()
#asyncio_thread.join(0.1)  # Give the thread some time to set up the loop

class Comet(pygame.sprite.Sprite):
    global_id_counter = 0

    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.image.load(os.path.join('assets/comets', 'comet_master.png')).convert_alpha()
        self.random_angle = random.choice([0, 90, 180, 270])
        self.image = pygame.transform.rotate(pygame.transform.scale(self.image, (size, size)), self.random_angle)
        self.rect = self.image.get_rect(topleft=pos)
        self.last_sent = pygame.time.get_ticks()  # Initialize last_sent properly
        self.update_freq = 1000  # Increase frequency if needed (ms)
        global global_id_counter
        self.id = Comet.global_id_counter + 1
        Comet.global_id_counter += 1

    def update(self, speed, scaling, horizontal_movement):
        self.rect.y -= int(1 * scaling * speed)
        self.rect.x += int(horizontal_movement * scaling * speed)
        current_time = pygame.time.get_ticks()

        # comment out to see if still lagging
        if current_time - self.last_sent > self.update_freq:
            self.update_visicon()
            self.last_sent = current_time

    def update_visicon(self):
        #message = f"{{\"method\": \"evaluate\", \"params\": [\"add-visicon-features\", \"compas-model\", [\"screen-x\", {self.rect.x}, \"screen-y\", {self.rect.y}], \"id\": 1}}"
        message = f"{{\"method\": \"evaluate\", \"params\":[\"add-visicon-features\", \"compas-model\", [\"screen-x\", {self.rect.x}, \"screen-y\", {self.rect.y}, \"comet-id\", {self.id}]], \"id\": 1}}"
        #message2 = '{"method": "evaluate", "params":["add-visicon-features", "compas-model", ["screen-x", 2, "screen-y", 2]], "id": 1}'
        #print("message2 is: " + message2)
        actr.rpc_interface.communicate_socket(sock=comet_socket, message=message)

        #asyncio.run_coroutine_threadsafe(monitor_output_key(), loop)
        message = {
        "method": "monitor",
        "params": ["output-key", "handle-output-key"]
        }
        #actr.rpc_interface.communicate_socket(sock=socket, message=json.dumps(message))

        #message = f"{{\"method\": \"monitor\", \"params\":[\"output-key\", \"press-key\"], \"id\": 3}}"
        #message = actr.rpc_interface.receive(socket)
        #return_msg = actr.rpc_interface.communicate_socket(sock=socket, message=message)
        #actr.rpc_interface.communicate_socket(sock=socket, message=message)
        message = actr.rpc_interface.receive(socket=move_socket)
        if message is not None and 'method' in message.keys() and 'params'in message.keys() and 'id' in message.keys():
            if message['method'] == 'evaluate':
                if message['params'][0] == "moveleft":
                    print("KEY PRESSED")
                    response_message = {
                    "result": ["result"],
                    "error": None,
                    "id": message['id']
                    }
                    actr.rpc_interface.send(move_socket, json.dumps(response_message))
    
        #print(f"return_msg is: {return_msg}")
"""
async def monitor_output_key():
    message = {
        "method": "monitor",
        "params": ["output-key", "press-key"]
    }
    response = await actr.rpc_interface.communicate(socket, json.dumps(message))
    print(response)

async def handle_output_key(params):
    # Handle the output-key event here
    print("Output-key event detected:", params)
"""