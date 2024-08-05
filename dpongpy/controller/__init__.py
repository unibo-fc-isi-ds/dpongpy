import pygame
from dpongpy.model import *
from dataclasses import dataclass
from enum import Enum
from typing import Protocol


class ControlEvent(Enum):
    PLAYER_JOIN = pygame.event.custom_type()
    PLAYER_LEAVE = pygame.event.custom_type()
    GAME_START = pygame.event.custom_type()
    GAME_OVER = pygame.QUIT
    PADDLE_MOVE = pygame.event.custom_type()
    TIME_ELAPSED = pygame.event.custom_type()


class PlayerAction(Enum):
    MOVE_UP = 0
    MOVE_DOWN = 1
    MOVE_RIGHT = 2
    MOVE_LEFT = 3
    STOP = 4
    QUIT = 5

    def to_direction(self):
        if 'MOVE_' in self.name:
            return Direction[self.name.split('_')[1]]
        elif self == PlayerAction.STOP:
            return Direction.NONE
        return None


@dataclass(frozen=True)
class ActionMap:
    move_up: int
    move_down: int
    move_left: int
    move_right: int
    quit: int = pygame.K_ESCAPE

    def to_key_map(self):
        return {getattr(self, name): PlayerAction[name.upper()] for name in self.__annotations__}

    @classmethod
    def wasd(cls):
        return cls(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)

    @classmethod
    def ijkl(cls):
        return cls(pygame.K_i, pygame.K_k, pygame.K_j, pygame.K_l)

    @classmethod
    def numpad(cls):
        return cls(pygame.K_KP8, pygame.K_KP2, pygame.K_KP4, pygame.K_KP6)

    @classmethod
    def arrow_keys(cls):
        return cls(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)

    @classmethod
    def all_mappings(cls):
        yield cls.wasd()
        yield cls.arrow_keys()
        yield cls.ijkl()
        yield cls.numpad()


class InputHandler(Protocol):
    def post_event(self, event: pygame.event.Event | ControlEvent, **kwargs):
        ...

    def key_pressed(self, key: int):
        ...

    def key_released(self, key: int):
        ...

    def time_elapsed(self, dt: float):
        ...

    def handle_inputs(self, dt=None):
        ...


class EventHandler(Protocol):
    def handle_events(self):
        ...

    def on_player_join(self, pong: Pong, paddle_index: int | Direction):
        ...

    def on_player_leave(self, pong: Pong, paddle_index: int):
        ...

    def on_game_start(self, pong: Pong):
        ...

    def on_game_over(self, pong: Pong):
        ...

    def on_paddle_move(self, pong: Pong, paddle_index: int | Direction, direction: Direction):
        ...

    def on_time_elapsed(self, pong: Pong, dt: float):
        ...
