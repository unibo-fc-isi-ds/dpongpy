import pygame
from dpongpy.log import logger
from dpongpy import PongGame, Settings
from dpongpy.model import *
from dpongpy.controller.local import *
from dpongpy.remote import Server
from dpongpy.remote.presentation import serialize, deserialize
import threading


class CoordinatorSidePongController(P)


class PongCoordinator(PongGame):

    DEFAULT_PORT = 12345

    def __init__(self, settings: Settings = None):
        super().__init__(settings)
        self.server = Server(self.settings.port or self.DEFAULT_PORT)
        self.thread = threading.Thread(target=self._handle_ingoing_messages, daemon=True)
        self.thread.start()

    def create_view(self):
        from dpongpy.view import ShowNothingPongView
        return ShowNothingPongView(self.pong)

    def create_controller(self):
        return super().create_controller()

    def at_each_run(self):
        pass

    def after_run(self):
        pass

    def before_run(self):
        pass

    def _handle_ingoing_messages(self):
        while self.running:
            message, sender = self.server.receive()
            logger.debug(f"receive message from {sender}:\n\t{message}")
            message = deserialize(message)
            assert isinstance(message, pygame.event.Event), f"Expected {pygame.event.Event}, got {type(message)}"
            pygame.event.post(message)
