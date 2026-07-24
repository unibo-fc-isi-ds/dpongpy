from dpongpy.log import logger
from dpongpy.remote import *
import os
import random
import socket

THRESHOLD_DGRAM_SIZE = 65536
UDP_DROP_RATE = float(os.environ.get("UDP_DROP_RATE", 0.0))
assert 0 <= UDP_DROP_RATE < 1

if UDP_DROP_RATE > 0:
    logger.warning(f"Drop rate for outgoing UDP messages is {UDP_DROP_RATE}")

def udp_socket(bind_to: Address | int = Address.any_local_port()) -> socket.socket:
    if isinstance(bind_to, int):
        bind_to = Address.localhost(bind_to)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if bind_to is not None:
        sock.bind(bind_to.as_tuple())
    sock.setblocking(False)
    return sock

def udp_send(sock: socket.socket, address: Address, payload: bytes | str) -> int:
    if isinstance(payload, str):
        payload = payload.encode()
    if len(payload) > THRESHOLD_DGRAM_SIZE:
        raise ValueError("UDP payload too large")
    if random.random() < UDP_DROP_RATE:
        logger.warning(f"Pretend send to {address}")
        return len(payload)
    return sock.sendto(payload, address.as_tuple())

def udp_receive(sock: socket.socket, decode=True):
    try:
        payload, address = sock.recvfrom(THRESHOLD_DGRAM_SIZE)
    except BlockingIOError:
        return None, None
    except OSError:
        return None, None
    address = Address(*address)
    if decode:
        payload = payload.decode()
    return payload, address

def has_message(sock: socket.socket) -> bool:
    try:
        sock.recvfrom(1, socket.MSG_PEEK)
        return True
    except (BlockingIOError, OSError):
        return False

class UdpSession(Session):
    def __init__(self, socket: socket.socket, remote_address: Address | tuple, first_message: str | bytes | None = None):
        self._socket = socket
        self._remote_address = Address(*remote_address) if isinstance(remote_address, tuple) else remote_address
        self._first_message = first_message

    @property
    def remote_address(self):
        return self._remote_address

    def send(self, payload: bytes | str):
        return udp_send(self._socket, self.remote_address, payload)

    def receive(self, decode=True):
        if self._first_message is not None:
            payload = self._first_message
            self._first_message = None
            return payload
        payload, address = udp_receive(self._socket, decode)
        if address is not None:
            self._remote_address = address
        return payload

    def close(self):
        try:
            self._socket.close()
        except OSError:
            pass

class UdpServer(Server):
    def __init__(self, port: int):
        self._socket = udp_socket(Address.local_port_on_any_interface(port))

    def receive(self, decode=True):
        return udp_receive(self._socket, decode)

    def send(self, address: Address, payload: bytes | str):
        return udp_send(self._socket, address, payload)

    def close(self):
        try:
            self._socket.close()
        except OSError:
            pass

class UdpClient(UdpSession):
    def __init__(self, remote_address: Address):
        super().__init__(udp_socket(), remote_address)
