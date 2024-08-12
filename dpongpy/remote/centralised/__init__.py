from pygame.event import Event
import pygame
from dpongpy import PongGame, Settings
from dpongpy.model import *
from dpongpy.controller import ControlEvent
from dpongpy.remote.udp import Server, Client
from dpongpy.remote.presentation import serialize, deserialize
import threading


DEFAULT_HOST = "localhost"
DEFAULT_PORT = 12345


class PongCoordinator(PongGame):

    def __init__(self, settings: Settings = None):
        settings = settings or Settings()
        settings.initial_paddles = []
        super().__init__(settings)
        self.pong.reset_ball((0, 0))
        self.server = Server(self.settings.port or DEFAULT_PORT)
        self.thread = threading.Thread(target=self._handle_ingoing_messages, daemon=True)
        self.thread.start()
        self._peers = set()
        self._lock = threading.RLock()

    def create_view(coordinator):
        from dpongpy.view import ShowNothingPongView
        from dpongpy.controller.local import ControlEvent

        class SendToPeersPongView(ShowNothingPongView):
            def render(self):
                event = coordinator.controller.create_event(ControlEvent.TIME_ELAPSED, dt=coordinator.dt, pong=self._pong)
                coordinator._broadcast_to_all_peers(event)

        return SendToPeersPongView(coordinator.pong)

    def create_controller(coordinator):
        from dpongpy.controller.local import PongEventHandler, InputHandler
        
        class Controller(PongEventHandler, InputHandler):
            def __init__(self, pong: Pong):
                PongEventHandler.__init__(self, pong)

            def on_player_join(self, pong: Pong, paddle_index: int | Direction):
                super().on_player_join(pong, paddle_index)
                pong.reset_ball()

            def on_player_leave(self, pong: Pong, paddle_index: Direction):
                if pong.has_paddle(paddle_index):
                    pong.remove_paddle(paddle_index)
                if len(pong.paddles) == 0:
                    self.on_game_over(pong)
                else:
                    pong.reset_ball()

            def on_game_over(self, pong: Pong):
                event = self.create_event(ControlEvent.GAME_OVER)
                coordinator._broadcast_to_all_peers(event)
                coordinator.stop()

            def handle_inputs(self, dt=None):
                self.time_elapsed(dt)

        return Controller(coordinator.pong)

    def before_run(self):
        logger.info("Coordinator starting")
        super().before_run()

    def at_each_run(self):
        pass

    def after_run(self):
        self.server.close()
        logger.info("Coordinator stopped gracefully")
        super().after_run()

    # def before_run(self):
    #     pass

    @property
    def peers(self):
        with self._lock:
            return set(self._peers)
    
    @peers.setter
    def peers(self, value):
        with self._lock:
            self._peers = set(value)

    def add_peer(self, peer):
        with self._lock:
            self._peers.add(peer)

    def _broadcast_to_all_peers(self, message):
        event = serialize(message)
        for peer in self.peers:
            self.server.send(payload=event, address=peer)

    def _handle_ingoing_messages(self):
        while self.running:
            message, sender = self.server.receive()
            if sender is not None:
                self.add_peer(sender)
                message = deserialize(message)
                assert isinstance(message, pygame.event.Event), f"Expected {pygame.event.Event}, got {type(message)}"
                pygame.event.post(message)
            elif self.running:
                logger.warn(f"Receive operation returned None: the server may have been closed ahead of time")


class PongTerminal(PongGame):

    def __init__(self, settings: Settings = None):
        settings = settings or Settings()
        assert len(settings.initial_paddles) == 1, "Only one paddle is allowed in terminal mode"
        super().__init__(settings)
        self.pong.reset_ball((0, 0))
        self.client = Client((self.settings.host or DEFAULT_HOST, self.settings.port or DEFAULT_PORT))

    def create_controller(terminal):
        from dpongpy.controller.local import PongInputHandler, EventHandler

        class Controller(PongInputHandler, EventHandler):
            def __init__(self, pong: Pong):
                PongInputHandler.__init__(self, pong)

            def post_event(self, event: Event | ControlEvent, **kwargs):
                event = self.create_event(event, **kwargs)
                terminal.client.send(serialize(event))
                if event.type == ControlEvent.PLAYER_LEAVE.value:
                    super().post_event(event, **kwargs)
                return event

            def handle_inputs(self, dt=None):
                return super().handle_inputs(dt=None)
            
            def handle_events(self):
                terminal._handle_ingoing_messages()
                for event in pygame.event.get():
                    if ControlEvent.TIME_ELAPSED.matches(event):
                        pong = event.dict["pong"]
                        self.on_time_elapsed(pong, dt=event.dict["dt"])
                    if ControlEvent.GAME_OVER.matches(event):
                        self.on_game_over(self._pong)

            def on_time_elapsed(self, pong: Pong, dt: float):
                terminal.pong.override(pong)

            def on_game_over(self, pong: Pong):
                terminal.stop()
        
        return Controller(terminal.pong)
    
    def _handle_ingoing_messages(self):
        if self.running:
            message = self.client.receive()
            if message is not None:
                message = deserialize(message)
                assert isinstance(message, pygame.event.Event), f"Expected {pygame.event.Event}, got {type(message)}"
                pygame.event.post(message)
            elif self.running:
                logger.warn(f"Receive operation returned None: the client may have been closed ahead of time")

    def before_run(self):
        logger.info("Terminal starting")
        super().before_run()
        self.controller.post_event(ControlEvent.PLAYER_JOIN, paddle_index=self.settings.initial_paddles[0])

    def after_run(self):
        self.client.close()
        logger.info("Terminal stopped gracefully")
        super().after_run()


def main_coordinator(settings = None):
    PongCoordinator(settings).run()


def main_terminal(settings = None):
    PongTerminal(settings).run()
