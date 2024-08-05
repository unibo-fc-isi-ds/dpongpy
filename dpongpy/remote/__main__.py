import sys
from dpongpy.remote import *

if len(sys.argv) == 3:
    remote = Address(*sys.argv[1:])
    local = Address.any_local_port()
elif len(sys.argv) == 2:
    remote = None
    local = Address.localhost(sys.argv[1])
else:
    print("Usage: python -m dpongpy.remote [ADDRESS] PORT")
    sys.exit(1)

if remote is None: # sever
    with Server(local.port) as server:
        print(f"Server listening on {local.port}")
        while True:
            payload, sender = server.receive()
            print(f'[{sender.ip}:{sender.port}]', payload.decode())
            response = input("> ")
            server.send(sender, response)
else: # client
    with Client(remote) as client:
        print(f"Connected to {remote}")
        while True:
            message = input("> ")
            client.send(message)
            response = client.receive()
            print(f'[{client.remote_address.ip}:{client.remote_address.port}]', response.decode())
