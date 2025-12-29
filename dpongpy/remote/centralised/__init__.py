from pygame.event import Event
import pygame
import time
from dpongpy import PongGame, Settings
from dpongpy.model import *
from dpongpy.controller import ControlEvent
from dpongpy.model import Direction, Pong
from dpongpy.remote.udp import UdpClient, UdpServer, Address
from dpongpy.remote.presentation import serialize, deserialize
import threading


DEFAULT_HOST = "localhost"
DEFAULT_PORT = 12345


class PongCoordinator(PongGame):

    def __init__(self, settings: Settings = None):
        settings = settings or Settings()
        settings.initial_paddles = []
        super().__init__(settings)
        self.pong.reset_ball(Vector2(0))
        self.server = UdpServer(self.settings.port or DEFAULT_PORT)
        self._thread_receiver = threading.Thread(target=self._handle_ingoing_messages, daemon=True)
        self._thread_receiver.start()
        self._peers: set[Address] = set()
        self._lock = threading.RLock()

    def create_view(coordinator):
        from dpongpy.view import ShowNothingPongView
        from dpongpy.controller.local import ControlEvent

        class SendToPeersPongView(ShowNothingPongView):
            def render(self):
                event = coordinator.controller.create_event(ControlEvent.TIME_ELAPSED, dt=coordinator.dt, status=self._pong)
                coordinator._broadcast_to_all_peers(event)

        return SendToPeersPongView(coordinator.pong)

    def create_controller(coordinator, paddle_commands):
        from dpongpy.controller.local import PongEventHandler, InputHandler

        class Controller(PongEventHandler, InputHandler):
            def __init__(self, pong: Pong):
                PongEventHandler.__init__(self, pong)

            def on_player_join(self, pong: Pong, paddle_index: Direction):
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
            try:
                message, sender = self.server.receive()
                if message is None: continue
                self.add_peer(sender)
                event = deserialize(message)
                pygame.event.post(event)
            except Exception as e:
                if not self.running: break
                logger.error(f"Errore ricezione: {e}")

class PongTerminal(PongGame):

    def __init__(self, settings: Settings = None):
        settings = settings or Settings()
        assert len(settings.initial_paddles) == 1, "Only one paddle is allowed in terminal mode"
        super().__init__(settings)
        self.pong.reset_ball(Vector2(0))
        self.client = UdpClient(Address(self.settings.host or DEFAULT_HOST, self.settings.port or DEFAULT_PORT))
        self.latest_remote_status = None #AGGIUNTA MIA, memorizzo l'ultimo stato remoto
        self.receiver_running = True #AGGIUNTA MIA, controllo il thread di ricezione
        threading.Thread(  #AGGIUNTA MIA
            target=self._receiver_loop,
            daemon=True
        ).start()

    def create_view(terminal):
        from dpongpy.view import ScreenPongView
        return ScreenPongView(terminal.pong, debug=True)


    def create_controller(terminal, paddle_commands = None):
        from dpongpy.controller.local import PongInputHandler, PongEventHandler

        class Controller(PongInputHandler, PongEventHandler):
            def __init__(self, pong: Pong, paddle_commands):
                PongInputHandler.__init__(self, pong, paddle_commands)
                PongEventHandler.__init__(self, pong)

            def post_event(self, event: Event | ControlEvent, **kwargs):
                event = super().post_event(event, **kwargs)
                if not ControlEvent.TIME_ELAPSED.matches(event):
                    terminal.client.send(serialize(event))
                return event

            def handle_inputs(self, dt=None):
                evt = self.create_event(
                    ControlEvent.TIME_ELAPSED,
                    dt=dt
                )
                pygame.event.post(evt)
                return super().handle_inputs(dt=None)

            def handle_events(self):
                #terminal._handle_ingoing_messages()   #AGGIUNTA MIA, RIMUOVO. INUTILE
                super().handle_events()

            def on_time_elapsed(self, pong: Pong, dt: float, status: Pong = None): # type: ignore[override] #AGGIUNTA MIA, lieve modifica
                if status is not None:
                    pong.override(status)
                else:
                    pong.update(dt)

            def on_player_leave(self, pong: Pong, paddle_index: Direction):
                terminal.stop()

            # All'interno di PongCoordinator.create_controller
            def on_paddle_move(self, pong: Pong, paddle_index: Direction, direction: Direction):
                super().on_paddle_move(pong, paddle_index, direction)

        return Controller(terminal.pong, paddle_commands)

    def _handle_ingoing_messages(self):    #LO RIMUOVO E' PROBLEMATICO
        pass

    def _receiver_loop(self): #AGGIUNTA MIA, nessun blocco
        while self.receiver_running:
            try:
                message = self.client.receive()
            except OSError:
                break #CHIUDO LA SOCKET
            if message is None:
                time.sleep(0.001)
                continue
            event = deserialize(message)
            pygame.event.post(event)

    def before_run(self):
        super().before_run()
        for paddle in self.pong.paddles:
            event = self.controller.create_event(ControlEvent.PLAYER_JOIN,paddle_index=paddle.side)
            self.client.send(serialize(event))
            self.pong.reset_ball()

    def after_run(self):
        self.running = False
        self.receiver_running = False
        self.client.close()
        super().after_run()


def main_coordinator(settings = None):
    PongCoordinator(settings).run()


def main_terminal(settings = None):
    PongTerminal(settings).run()
