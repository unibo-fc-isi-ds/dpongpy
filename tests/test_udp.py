import unittest
from dpongpy.remote.udp import *
from typing import Optional


class BaseUdpTest(unittest.TestCase):
    TEST_PORT = 54321
    server_address = Address('localhost', TEST_PORT)
    message1 = "Hello, World!"
    message2 = "Goodbye, World!"
    server: Optional[UdpServer] = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.server = UdpServer(cls.TEST_PORT)

    @classmethod
    def tearDownClass(cls) -> None:
        if cls.server is not None:
            cls.server.close()

    def assertIsLocalEndpoint(self, address):
        self.assertIn(address.ip, {'localhost', '127.0.0.1', '0.0.0.0'})
        self.assertIn(address.port, range(1, 1 << 16))


class TestUdpClientAndServer(BaseUdpTest):
    def test_server_is_initially_bound(self):
        self.assertEqual(self.server.local_address, Address('0.0.0.0', self.TEST_PORT))

    def test_client_is_initially_bound(self):
        with UdpClient(self.server_address) as client:
            self.assertTrue(client.remote_address.equivalent_to(self.server_address))
            self.assertIsLocalEndpoint(client.local_address)

    def test_communication(self):
        with UdpClient(self.server_address) as client1:
            client1.send(self.message1)
            message, sender1 = self.server.receive()
            self.assertEqual(self.message1, message)
            self.assertIsLocalEndpoint(sender1)
            with UdpClient(self.server_address) as client2:
                client2.send(self.message2)
                message, sender2 = self.server.receive()
                self.assertEqual(self.message2, message)
                self.assertIsLocalEndpoint(sender2)
            self.assertNotEqual(sender1, sender2)


class TestUdpServerListening(BaseUdpTest):
    def test_server_listening(self):
        with UdpClient(self.server_address) as client:
            client.send(self.message1)
            with self.server.listen() as server_session:
                self.assertEqual(server_session.remote_address.port, client.local_address.port)
                self.assertEqual(server_session.receive(), self.message1)
                server_session.send(self.message2)
                self.assertEqual(client.receive(), self.message2)   
