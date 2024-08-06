from pygame.event import Event
from dpongpy.controller import ControlEvent, Direction, Pong
import pygame
from dpongpy import PongGame, Settings
from dpongpy.model import *
from dpongpy.remote import Server, Client
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
                event = coordinator.controller.create_event(ControlEvent.TIME_ELAPSED, dt=coordinator.dt, pong=coordinator.pong)
                event = serialize(event)
                for peer in coordinator.peers:
                    coordinator.server.send(payload=event, address=peer)

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
                coordinator.stop()

            def handle_inputs(self, dt=None):
                self.time_elapsed(dt)

        return Controller(coordinator.pong)

    def at_each_run(self):
        pass

    def after_run(self):
        super().after_run()
        self.server.close()

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

    def _handle_ingoing_messages(self):
        while self.running:
            message, sender = self.server.receive()
            self.add_peer(sender)
            message = deserialize(message)
            assert isinstance(message, pygame.event.Event), f"Expected {pygame.event.Event}, got {type(message)}"
            pygame.event.post(message)


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
                        terminal.pong.override(pong)
        
        return Controller(terminal.pong)
    
    def _handle_ingoing_messages(self):
        if self.running:
            message = self.client.receive()
            message = deserialize(message)
            assert isinstance(message, pygame.event.Event), f"Expected {pygame.event.Event}, got {type(message)}"
            pygame.event.post(message)

    def before_run(self):
        super().before_run()
        self.controller.post_event(ControlEvent.PLAYER_JOIN, paddle_index=self.settings.initial_paddles[0])

    def after_run(self):
        super().after_run()
        self.server.close()


def main_coordinator(settings = None):
    PongCoordinator(settings).run()


def main_terminal(settings = None):
    PongTerminal(settings).run()
