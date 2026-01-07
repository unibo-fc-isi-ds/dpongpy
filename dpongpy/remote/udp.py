from dpongpy.log import logger
from dpongpy.remote import *
import os
import random


THRESHOLD_DGRAM_SIZE = 65536
UDP_DROP_RATE = float(os.environ.get("UDP_DROP_RATE", 0.0))
assert 0 <= UDP_DROP_RATE < 1, "Drop rate for outgoing UDP messages must be between 0 (included) and 1 (excluded)"
# UDP_DROP_RATE = 0.2
if UDP_DROP_RATE > 0:
    logger.warning(f"Drop rate for outgoing UDP messages is {UDP_DROP_RATE}")


def udp_socket(bind_to: Address | int = Address.any_local_port()) -> socket.socket:
    if isinstance(bind_to, int):
        bind_to = Address.localhost(bind_to)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if bind_to is not None:
        sock.bind(bind_to.as_tuple()) # type: ignore[union-attr]
        logger.debug(f"Bind UDP socket to {sock.getsockname()}")
    return sock


def udp_send(sock: socket.socket, address:Address, payload: bytes | str) -> int:
    if isinstance(payload, str):
        payload = payload.encode()
    if len(payload) > THRESHOLD_DGRAM_SIZE:
        raise ValueError(f"Payload size must be less than {THRESHOLD_DGRAM_SIZE} bytes ({THRESHOLD_DGRAM_SIZE / 1024} KiB)")
    if random.uniform(0, 1) < UDP_DROP_RATE:
        result = len(payload)
        logger.warning(f"Pretend to send {result} bytes to {address}: {payload!r}")
    else:
        result = sock.sendto(payload, address.as_tuple())
        logger.debug(f"Sent {result} bytes to {address}: {payload!r}")
    return result


def udp_receive(sock: socket.socket, decode=True) -> tuple[str | bytes | None, Address | None]:
    try:
        payload, address = sock.recvfrom(THRESHOLD_DGRAM_SIZE)
    except ConnectionResetError:
        return None, None # just the client ending connection
    address = Address(*address)
    logger.debug(f"Received {len(payload)} bytes from {address}: {payload!r}")
    if decode:
        payload = payload.decode() # type: ignore[assignment]
    return payload, address


class UdpSession(Session):
    def __init__(self,
                 socket: socket.socket,
                 remote_address: Address | tuple,
                 first_message: str | bytes | None = None):
        assert socket is not None, "Socket must not be None"
        self._socket = socket
        assert remote_address is not None, "Remote address must not be None"
        self._remote_address = Address(*remote_address) if isinstance(remote_address, tuple) else remote_address
        self._received_messages = 0 if first_message is None else 1
        self._first_message = first_message

    @property
    def remote_address(self):
        return self._remote_address

    @property
    def local_address(self):
        return Address(*self._socket.getsockname())

    def send(self, payload: bytes | str):
        return udp_send(self._socket, self.remote_address, payload)

    def receive(self, decode=True):
        if self._first_message is not None:
            payload = self._first_message
            if decode and isinstance(payload, bytes):
                payload = payload.decode()
            self._first_message = None
            return payload
        payload, address = udp_receive(self._socket, decode)
        if address is not None:
            if self._received_messages == 0:
                self._remote_address = address
            assert address.equivalent_to(self.remote_address), f"Received packet from unexpected party {address}"
            return payload
        return None

    def close(self):
        self._socket.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class UdpServer(Server):
    def __init__(self, port: int):
        self._address = Address.local_port_on_any_interface(port)
        self._socket = udp_socket(self._address)

    @property
    def local_address(self):
        return Address(*self._socket.getsockname())

    def listen(self) -> UdpSession:
        payload, address = udp_receive(self._socket, True)
        assert address is not None, "Received packet from unknown party"
        return UdpSession(
            socket=udp_socket(),
            remote_address=address,
            first_message=payload
        )

    def receive(self, decode=True) -> tuple[str | bytes | None, Address | None]:
        return udp_receive(self._socket, decode)

    def send(self, address: Address, payload: bytes | str):
        return udp_send(self._socket, address, payload)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self._socket.close()


class UdpClient(UdpSession):
    def __init__(self, remote_address: Address):
        super().__init__(udp_socket(), remote_address)
