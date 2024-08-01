import pygame
from dpongpy.model import *


class PongController:
    def __init__(self, pong: Pong, on_quit=None):
        self._pong = pong
        self.on_quit = on_quit or (lambda _: None)

    def time_elapsed(self, dt: float):
        self._pong.update(dt)

    def post_event(self, event: pygame.event.Event):
        pygame.event.post(event)

    def key_pressed(self, key: int):
        if key == pygame.K_w:
            self.on_paddle_move(self._pong, 0, Direction.UP)
        if key == pygame.K_s:
            self.on_paddle_move(self._pong,0, Direction.DOWN)
        if key == pygame.K_UP:
            self.on_paddle_move(self._pong,1, Direction.UP)
        if key == pygame.K_DOWN:
            self.on_paddle_move(self._pong,1, Direction.DOWN)
        if key == pygame.K_ESCAPE:
            self.post_event(pygame.event.Event(pygame.QUIT))

    def key_released(self, key: int):
        if key == pygame.K_w:
            self.on_paddle_stop(self._pong, 0)
        if key == pygame.K_s:
            self.on_paddle_stop(self._pong, 0)
        if key == pygame.K_UP:
            self.on_paddle_stop(self._pong, 1)
        if key == pygame.K_DOWN:
            self.on_paddle_stop(self._pong, 1)

    def on_paddle_move(self, pong: Pong, paddle_index: int, direction: Direction):
        pong.move_paddle(paddle_index, direction)

    def on_paddle_stop(self, pong: Pong, paddle_index: int):
        pong.stop_paddle(paddle_index)

    def update(self, dt: float):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.on_quit(self._pong)
            elif event.type == pygame.KEYDOWN:
                self.key_pressed(event.key)
            elif event.type == pygame.KEYUP:
                self.key_released(event.key)

        self.time_elapsed(dt)
