import pygame

from .model import *
from pygame import draw, Surface, Rect
from typing import Iterable, Protocol


def rect(rectangle: Rectangle) -> pygame.Rect:
    return pygame.Rect(rectangle.top_left, rectangle.size)


class PongView(Protocol):
    def __init__(self, pong: Pong):
        pass

    def render(self):
        ...


class ShowNothingPongView(PongView):
    def render(self):
        pass


class ScreenPongView(PongView):
    debug_color = "green"

    def __init__(self, pong: Pong, screen: Surface = None, debug: bool = False):
        self._pong = pong
        self._screen = screen or pygame.display.set_mode(pong.size)
        self._debug = debug

    def __getattr__(self, name):
        if not name.startswith("draw_"):
            raise AttributeError(f"{type(self).__name__} has no attribute '{name}'")
        name = name[5:]
        debug = False
        if name.startswith("debug_"):
            name = name[6:]
            debug = True
        function = getattr(draw, name)
        if debug:
            def debug_draw(*args, **kwargs):
                if self._debug:
                    function(self._screen, self.debug_color, *args, **kwargs)
            return debug_draw
        return lambda *args, **kwargs: function(self._screen, *args, **kwargs)

    def render(self):
        self._screen.fill("black")
        self.render_arena(self._pong)
        self.render_ball(self._pong.ball)
        self.render_paddles(self._pong.paddles)

    def render_arena(self, pong: Pong):
        self.draw_debug_line((0, pong.height / 2), (pong.width, pong.height / 2), width=1)
        self.draw_debug_line((pong.width / 2, 0), (pong.width / 2, pong.height), width=1)
        self.draw_debug_rect(Rect((0, 0), pong.size), width=1)

    def render_bounds(self, obj: GameObject):
        self.draw_debug_rect(rect(obj.bounding_box), width=1)

    def render_speed(self, obj: GameObject):
        if self._debug:
            self.draw_line("blue", obj.position, obj.position + obj.speed, width=2)

    def render_ball(self, ball: Ball):
        self.draw_ellipse("white", rect(ball.bounding_box), width=0)
        self.render_bounds(ball)
        self.render_speed(ball)

    def render_paddles(self, paddles: Iterable[Paddle]):
        for paddle in paddles:
            self.render_paddle(paddle)

    def render_paddle(self, paddle: Paddle):
        self.draw_rect("white", rect(paddle.bounding_box), width=0)
        self.render_bounds(paddle)
        self.render_speed(paddle)
