from dpongpy.log import logger
from dpongpy.remote import *
from functools import cache
import threading
import queue


def tcp_socket(bind_to: Address | int = Address.any_local_port()) -> socket.socket:
    if isinstance(bind_to, int):
        bind_to = Address.localhost(bind_to)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if bind_to is not None:
        sock.bind(bind_to.as_tuple())
        logger.debug(f"Bind TCP socket to {sock.getsockname()}")
    return sock


@cache
def tcp_get_remote_address(sock: socket.socket) -> Address:
    return Address(*sock.getpeername())


def tcp_send(sock: socket.socket, payload: bytes | str) -> int:
    if isinstance(payload, str):
        payload = payload.encode()
    length = len(payload).to_bytes(4, 'big')
    result: int = sock.sendall(payload + length)
    actual_address = tcp_get_remote_address(sock)
    logger.debug(f"Sent {result} bytes to {actual_address}: {payload}")
    return result


def tcp_receive(sock: socket.socket, decode=True) -> tuple[str | bytes, Address]:
    length = int.from_bytes(sock.recv(4), 'big')
    payload = sock.recv(length)
    address = tcp_get_remote_address(sock)
    logger.debug(f"Received {len(payload)} bytes from {address}: {payload}")
    if decode:
        payload = payload.decode()
    return payload, address


def tcp_accept(sock: socket.socket) -> tuple[socket.socket, Address]:
    socket, address = sock.accept()
    logger.debug(f"Accepted connection from {address}")
    return socket, Address(*address)


def tcp_connect(sock: socket.socket, address: Address) -> tuple[socket.socket, Address]:
    sock.connect(address.as_tuple())
    logger.debug(f"Connected to {address}")
    return sock, address


class Session(Session):

    def __init__(self, socket: socket.socket, remote_address: Address = None):
        assert socket is not None, "Socket must not be None"
        self._socket = socket
        self._remote_address = remote_address
        self._thread_receiver = threading.Thread(target=self.__handle_ingoing_messages)
        if remote_address is None:
            self._thread_receiver.start()

    def _handle_new_message(self, data):
        raise NotImplementedError

    def __handle_ingoing_messages(self):
        error = None
        try:
            while not self._socket._closed:
                message, address = tcp_receive(self._socket, decode=False)
                if address is not None:
                    self._handle_new_message((message, address, None))
                else:
                    break
        except Exception as e:
            error = e
            logger.error(error)
        finally:
            self._handle_new_message((None, None, error))

    @property
    def remote_address(self):
        return self._remote_address or tcp_get_remote_address(socket)

    @property
    def local_address(self):
        return Address(*self._socket.getsockname())

    def send(self, payload: bytes | str):
        return tcp_send(self._socket, payload)
    
    def close(self):
        self._socket.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __eq__(self, other):
        return isinstance(other, Session) and self._socket == other._socket

    def __hash__(self):
        return hash(self._socket)


class SyncSession(Session):
    def __init__(self, socket: socket.socket, remote_address: Address = None):
        super().__init__(socket, remote_address)
        self._inbox = queue.Queue()

    def _handle_new_message(self, message):
        self._inbox.put(message)

    def receive(self, decode=True):
        if self._inbox.qsize() == 0 and self._socket._closed:
            raise OSError("Socket is closed")
        payload, address, error = self._inbox.get()
        if error is not None:
            raise error
        if address is None:
            address = self.remote_address
        assert address.equivalent_to(self.remote_address), f"Received packet from unexpected party {address}"
        return payload


class AsyncSession(Session):
    def __init__(self, socket: socket.socket, callback, remote_address: Address = None):
        super().__init__(socket, remote_address)
        self._callback = callback

    def _handle_new_message(self, message):
        self._callback(*message)

    def receive(self, decode=True):
        raise NotImplementedError("Sync receive is not supported in asynchronous sessions")


class Server(Server):
    def __init__(self, port: int):
        self._address = Address.local_port_on_any_interface(port)
        self._socket = tcp_socket(self._address)
        self._socket.listen()
        self.listening = True
        self._thread_connections = threading.Thread(target=self.__handle_ingoing_connections)
        self._sessions: dict[Address, AsyncSession] = dict()
        self._inbox = queue.Queue()

    def __handle_ingoing_connections(self):
        while self.listening:
            session = self.listen(on_message_received=self.__handle_ingoing_message)
            self._sessions[session.remote_address] = session

    def __handle_ingoing_message(self, payload: bytes | str, address: Address, error: Exception):
        self._inbox.put((payload, address, error))

    def listen(self, on_message_received = None) -> Session:
        socket, address = tcp_accept(self._socket)
        if on_message_received is None:
            return SyncSession(socket)
        else:
            return AsyncSession(socket, on_message_received)

    def receive(self, decode=True) -> tuple[str | bytes, Address]:
        payload, address, error = self._inbox.get()
        if error is not None:
            raise error
        return payload, address

    def send(self, address: Address, payload: bytes | str):
        return self._sessions[address].send(payload)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        for session in self._sessions.values():
            session.close()
        self._socket.close()


class Client(SyncSession):
    def __init__(self, remote_address: Address):
        assert remote_address is not None, "Remote address must not be None"
        super().__init__(tcp_socket(), remote_address)

    def connect(self):
        tcp_connect(self._socket, self.remote_address)
        self._thread_receiver.start()
        return self
