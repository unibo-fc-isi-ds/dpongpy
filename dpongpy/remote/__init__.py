import socket
from dpongpy.log import logger
from dataclasses import dataclass, field


@dataclass(unsafe_hash=True)
class Address:
    host: str = field()
    port: int

    def __post_init__(self):
        self._ip = None
        if isinstance(self.port, str):
            self.port = int(self.port)
        assert 0 <= self.port <= 65535, "Port number must be between 0 and 65535"
        self.host = (self.host or '0.0.0.0').strip()

    def __str__(self):
        return f"{self.host}:{self.port}"

    def __repr__(self):
        return f"{type(self).__name__}(host={self.host}, ip={self.ip}, port={self.port})"

    @property
    def ip(self):
        if self._ip is None:
            self._ip = socket.gethostbyname(self.host)
        return self._ip

    def equivalent_to(self, other):
        return self.ip == other.ip and self.port == other.port

    @classmethod
    def parse(cls, address: str):
        host, port = address.split(":")
        return cls(host, int(port))
    
    @classmethod
    def local_port_on_any_interface(cls, port: int):
        return cls("0.0.0.0", port)

    @classmethod
    def localhost(cls, port: int):
        return cls("localhost", port)

    @classmethod
    def any_local_port(cls):
        return cls("", 0)

    def as_tuple(self):
        return self.ip, self.port


THRESHOLD_DGRAM_SIZE = 65536


def udp_socket(bind_to: Address | int = Address.any_local_port()) -> socket.socket:
    if isinstance(bind_to, int):
        bind_to = Address.localhost(bind_to)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if bind_to is not None:
        sock.bind(bind_to.as_tuple())
        logger.debug(f"Bind UDP socket to {sock.getsockname()}")
    return sock


def udp_send(sock: socket.socket, address:Address, payload: bytes | str) -> int:
    if isinstance(payload, str):
        payload = payload.encode()
    if len(payload) > THRESHOLD_DGRAM_SIZE:
        raise ValueError(f"Payload size must be less than {THRESHOLD_DGRAM_SIZE} bytes ({THRESHOLD_DGRAM_SIZE / 1024} KiB)")
    result = sock.sendto(payload, address.as_tuple())
    logger.debug(f"Sent {result} bytes to {address}: {payload}")
    return result


def udp_receive(sock: socket.socket, decode=True) -> tuple[str | bytes, Address]:
    payload, address = sock.recvfrom(THRESHOLD_DGRAM_SIZE)
    address = Address(*address)
    logger.debug(f"Received {len(payload)} bytes from {address}: {payload}")
    if decode:
        payload = payload.decode()
    return payload, address


class Session:
    def __init__(self,
                 socket: socket.socket,
                 remote_address: Address | tuple,
                 first_message: str | bytes = None):
        assert socket is not None, "Socket must not be None"
        self._socket = socket
        assert remote_address is not None, "Remote address must not be None"
        self.remote_address = Address(*remote_address) if isinstance(remote_address, tuple) else remote_address
        self._received_messages = 0 if first_message is None else 1
        self._first_message = first_message

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
        if self._received_messages == 0:
            self.remote_address = address
        assert address.equivalent_to(self.remote_address), f"Received packet from unexpected party {address}"
        return payload
    
    def close(self):
        self._socket.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class Server:
    _session_class = Session

    def __init__(self, port: int):
        self._address = Address.local_port_on_any_interface(port)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.bind(self._address.as_tuple())

    def listen(self) -> Session:
        payload, address = udp_receive(self._socket, True)
        return Session(
            socket=udp_socket(),
            remote_address=address,
            first_message=payload
        )

    def receive(self, decode=True) -> tuple[str | bytes, Address]:
        return udp_receive(self._socket, decode)

    def send(self, address: Address, payload: bytes | str):
        return udp_send(self._socket, address, payload)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self._socket.close()


class Client(Session):
    def __init__(self, remote_address: Address):
        super().__init__(udp_socket(), remote_address)
