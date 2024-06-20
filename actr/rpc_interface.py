import json
import asyncio
import socket
import os
import select


def start_connection():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with open(os.path.expanduser("~/act-r-port-num.txt"), 'r') as f:
        port = int(f.readline())
    
    with open(os.path.expanduser("~/act-r-address.txt"), 'r') as f:
        host = f.readline()
    sock.connect((host, port))

    sock.setblocking(0)

    return sock


# Send message
def send(socket,message):
    m = message + chr(4)
    socket.sendall(m.encode('utf-8'))



import select
import json



def receive(socket):
    buffer= ''
    try:
    #while not chr(4) in buffer:
        while not chr(4) in buffer:
            data = socket.recv(1)
            buffer += data.decode('utf-8')
    
        return json.loads(buffer[0:-1])
    except BlockingIOError:
        # No more data available to read
        return


"""
def receive(socket, timeout=0.02):
    buffer = ''
    try:
        # Use select to poll the socket with a timeout
        ready_to_read, writelist, errorlist = select.select([socket], [], [], timeout)
        print("PRINT")
        print(ready_to_read, writelist, errorlist)
        if ready_to_read:
            buffer= ''
            while not chr(4) in buffer:
                data = socket.recv(1)
                buffer += data.decode('utf-8')
            print("BUFFER PRINT")
            print(buffer)
            return json.loads(buffer[0:-1])

        else:
            # Timeout occurred, no data available to read
            print("Timeout: No data received within the specified timeout period.")
            return None
    except BlockingIOError:
        # No more data available to read
        pass
    except ConnectionResetError as e:
        print(f"Connection reset error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

    return None
"""

"""
def receive(socket):
    buffer = ''
    
    # Use select to poll the socket with no timeout (immediate return)
    ready_to_read, _, _ = select.select([socket], [], [], 0)
    
    if ready_to_read:
        try:
            while True:
                data = socket.recv(1)  # Read up to 1024 bytes at a time
                if not data:
                    # Connection closed by the client
                    break
                
                buffer += data.decode('utf-8')
                
                if chr(4) in buffer:
                    # End-of-transmission character found
                    message, buffer = buffer.split(chr(4), 1)
                    return json.loads(message)
        except BlockingIOError:
            # No more data available to read
            pass
        except (ConnectionResetError, json.JSONDecodeError) as e:
            print(f"Error receiving data: {e}")
            return None

    return None
"""

"""
def receive(socket, timeout=0.1):
    buffer = ''
    try:
        while True:
            # Use select to poll the socket with a timeout
            ready_to_read, _, _ = select.select([socket], [], [], timeout)
            if ready_to_read:
                data = socket.recv(1024)  # Read up to 1024 bytes at a time
                if not data:
                    # Connection closed by the server
                    print("Connection closed by the server")
                    return None

                buffer += data.decode('utf-8')

                if chr(4) in buffer:
                    # End-of-transmission character found
                    message, buffer = buffer.split(chr(4), 1)
                    return json.loads(message)
            else:
                # Timeout occurred, no data available to read
                print("Timeout: No data received within the specified timeout period.")
                return None
    except BlockingIOError:
        # No more data available to read
        pass
    except (ConnectionResetError, json.JSONDecodeError) as e:
        print(f"Error receiving data: {e}")
        return None

    return None
"""

def communicate_socket(sock, message):
    send(sock, message)
    message = receive(sock)

    return message
