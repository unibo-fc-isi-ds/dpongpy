from dpongpy.controller import *


class PongInputHandler(InputHandler):
    def __init__(self, pong: Pong, paddles_commands: dict[Direction, ActionMap] = None):
        self._pong = pong
        if paddles_commands is None:
            paddles_commands = dict()
            mappings = iter(ActionMap.all_mappings())
            for paddle in pong.paddles:
                paddles_commands[paddle.side] = next(mappings)
        self._paddles_commands = paddles_commands
        assert len(self._pong.paddles) == len(self._paddles_commands), "Number of paddles and commands must match"

    def post_event(self, event: pygame.event.Event | ControlEvent, **kwargs):
        if isinstance(event, ControlEvent):
            event = pygame.event.Event(event.value, **kwargs)
        elif isinstance(event, pygame.event.Event) and event.dict != kwargs:
            data = event.dict
            data.update(kwargs)
            event = pygame.event.Event(event.type, data)
        pygame.event.post(event)

    def _get_paddle_actions(self, key: int) -> dict[Direction, PlayerAction]:
        result = dict()
        for side, paddle_commands in self._paddles_commands.items():
            key_map = paddle_commands.to_key_map()
            if key in key_map:
                result[side] = key_map[key]
        return result

    def key_pressed(self, key: int):
        for paddle_index, action in self._get_paddle_actions(key).items():
            if action in {PlayerAction.MOVE_UP, PlayerAction.MOVE_DOWN}:
                self.post_event(ControlEvent.PADDLE_MOVE, paddle_index=paddle_index, direction=action.to_direction())
            elif action == PlayerAction.QUIT:
                self.post_event(ControlEvent.PLAYER_LEAVE, paddle_index=paddle_index)

    def key_released(self, key: int):
        for paddle_index, action in self._get_paddle_actions(key).items():
            if action in {PlayerAction.MOVE_UP, PlayerAction.MOVE_DOWN}:
                self.post_event(ControlEvent.PADDLE_MOVE, paddle_index=paddle_index, direction=Direction.NONE)

    def time_elapsed(self, dt: float):
        self.post_event(ControlEvent.TIME_ELAPSED, dt=dt)

    def handle_inputs(self, dt=None):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.key_pressed(event.key)
            elif event.type == pygame.KEYUP:
                self.key_released(event.key)
        if dt is not None:
            self.time_elapsed(dt)


class PongEventHandler(EventHandler):
    def __init__(self, pong: Pong):
        self._pong = pong

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == ControlEvent.PLAYER_JOIN.value:
                self.on_player_join(self._pong, **event.dict)
            elif event.type == ControlEvent.PLAYER_LEAVE.value:
                self.on_player_leave(self._pong, **event.dict)
            elif event.type == ControlEvent.GAME_START.value:
                self.on_game_start(self._pong)
            elif event.type == ControlEvent.GAME_OVER.value:
                self.on_game_over(self._pong)
            elif event.type == ControlEvent.PADDLE_MOVE.value:
                self.on_paddle_move(self._pong, **event.dict)
            elif event.type == ControlEvent.TIME_ELAPSED.value:
                self.on_time_elapsed(self._pong, **event.dict)

    def on_player_join(self, pong: Pong, paddle_index: int | Direction):
        pong.add_paddle(paddle_index)

    def on_player_leave(self, pong: Pong, paddle_index: int):
        self.on_game_over(pong)

    def on_game_start(self, pong: Pong):
        pass

    def on_game_over(self, pong: Pong):
        pass

    def on_paddle_move(self, pong: Pong, paddle_index: int | Direction, direction: Direction):
        pong.move_paddle(paddle_index, direction)

    def on_time_elapsed(self, pong: Pong, dt: float):
        pong.update(dt)


class PongLocalController(PongInputHandler, PongEventHandler):
    def __init__(self, pong: Pong, paddles_commands: list[ActionMap] = None):
        PongInputHandler.__init__(self, pong, paddles_commands)
        PongEventHandler.__init__(self, pong)
