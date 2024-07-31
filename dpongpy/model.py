from dpongpy import Vector2
from dataclasses import dataclass, field
from random import Random
from enum import Enum
# from reactivex.subject import Subject
import math


class Direction(Enum):
    UP = Vector2(0, -1)
    DOWN = Vector2(0, 1)
    LEFT = Vector2(-1, 0)
    RIGHT = Vector2(1, 0)

    @property
    def is_vertical(self) -> bool:
        return self.value.x == 0
    
    @property
    def is_horizontal(self) -> bool:
        return self.value.y == 0


@dataclass
class Rectangle:
    min: Vector2
    max: Vector2

    @property
    def size(self) -> Vector2:
        return self.max - self.min
    
    @property
    def position(self) -> Vector2:
        return (self.min + self.max) / 2

    def __post_init__(self):
        fst, snd = Vector2(self.min), Vector2(self.max)
        self.min = Vector2(min(fst.x, snd.x), min(fst.y, snd.y))
        self.max = Vector2(max(fst.x, snd.x), max(fst.y, snd.y))

    def overlaps(self, other: 'Rectangle') -> bool:
        return self.min.x <= other.max.x and self.max.x >= other.min.x and self.min.y <= other.max.y and self.max.y >= other.min.y
    
    def is_inside(self, other: 'Rectangle') -> bool:
        return self.min.x >= other.min.x and self.max.x <= other.max.x and self.min.y >= other.min.y and self.max.y <= other.max.y
    
    def __contains__(self, other: 'Rectangle') -> bool:
        return other.is_inside(self)
    
    def intersection_with(self, other: 'Rectangle') -> 'Rectangle':
        if self.overlaps(other):
            return Rectangle(
                Vector2(max(self.min.x, other.min.x), max(self.min.y, other.min.y)), 
                Vector2(min(self.max.x, other.max.x), min(self.max.y, other.max.y))
            )
        return None

    def hits(self, other: 'Rectangle') -> dict[Direction, float]:
        result = dict()
        intersection = self.intersection_with(other)
        if intersection is not None:
            if other.min.x < self.min.x:
                result[Direction.LEFT] = intersection.size.x
            if other.max.x > self.max.x:
                result[Direction.RIGHT] = intersection.size.x
            if other.min.y < self.min.y:
                result[Direction.UP] = intersection.size.y
            if other.max.y > self.max.y:
                result[Direction.DOWN] = intersection.size.y
        return result


@dataclass
class GameObject:
    size: Vector2
    position: Vector2 = field(default_factory=Vector2)
    speed: Vector2 = field(default_factory=Vector2)
    name: str = field(default=None)

    def __post_init__(self):
        if self.name is None:
            self.name = self.__class__.__name__.lower()

    @property
    def bounding_box(self) -> Rectangle:
        half_size = self.size / 2
        return Rectangle(self.position - half_size, self.position + half_size)

    def update(self, delta_time: float):
        self.position = self.position + self.speed * delta_time


for method_name in ['overlaps', 'is_inside', '__contains__', 'intersection_with', 'hits']:
    def method(self: GameObject, other: GameObject | Rectangle):
        if isinstance(other, GameObject):
            other = other.bounding_box
        return getattr(Rectangle, method_name)(self.bounding_box, other)
    setattr(GameObject, method_name, method)


class Ball(GameObject):
    pass


class Paddle(GameObject):
    pass

@dataclass
class Config:
    paddle_ratio: Vector2 = field(default_factory=lambda: Vector2(0.1, 0.01))
    ball_ratio: float = 0.05
    ball_speed_ratio: float = 0.1
    paddle_speed_ratio: float = 0.05
    paddle_padding: float = 0.05


@dataclass
class Table:
    size: Vector2
    borders: dict[Direction, GameObject] = field(init=False)

    def __post_init__(self):
        borders = dict()
        borders[Direction.UP] = Rectangle(Vector2(-self.size.x, 0), Vector2(self.size.x * 2, -self.size.y))
        borders[Direction.DOWN] = Rectangle(Vector2(-self.size.x, self.size.y), Vector2(self.size.x * 2, self.size.y * 2))
        borders[Direction.LEFT] = Rectangle(Vector2(0, -self.size.y), Vector2(-self.size.x, self.size.y * 2))
        borders[Direction.RIGHT] = Rectangle(Vector2(self.size.x, -self.size.y), Vector2(self.size.x * 2, self.size.y * 2))
        self.borders = dict()
        for dir, rect in borders.items():
            self.borders[dir] = GameObject(
                size=rect.size,
                position=rect.position,
                name=f"border_{dir.name.lower()}"
            )


@dataclass
class Pong:
    size: Vector2
    config: Config = field(default_factory=Config)
    ball: Ball = field(init=False)
    paddles: list[Paddle] = field(init=False)
    table: Table = field(init=False)
    random: Random = field(default_factory=Random)

    def __post_init__(self):
        self.size = Vector2(self.size)
        assert self.size.x > 0 and self.size.y > 0, "Size must be greater than 0"
        self.ball = self._init_ball()
        self.paddles = self._init_paddles()
        self.table = Table(self.size)

    @property
    def _hittable_objects(self) -> list[GameObject]:
        return [paddle for paddle in self.paddles] + list(self.table.borders.values())

    def _init_ball(self) -> Ball:
        min_dimension = min(*self.size)
        ball_size = Vector2(min_dimension * self.config.ball_ratio)
        ball = Ball(size=ball_size, position=self.size / 2)
        polar_speed = (min_dimension * self.config.ball_speed_ratio, self.random.uniform(0, 2 * math.pi))
        ball.speed = Vector2.from_polar(polar_speed)
        return ball
    
    def _init_paddles(self) -> list[Paddle]:
        paddle_size = self.size.elementwise() * self.config.paddle_ratio
        padding = self.size.x * self.config.paddle_padding + paddle_size.x / 2
        position1 = Vector2(padding, self.size.y / 2)
        position2 = Vector2(self.size.x - padding, self.size.y / 2)
        return (
            Paddle(size=paddle_size, position=position1, name="paddle_1"),
            Paddle(size=paddle_size, position=position2, name="paddle_2")
        )

    def update(self, delta_time: float):
        self.ball.update(delta_time)
        for paddle in self.paddles:
            paddle.update(delta_time)
        self._handle_collisions()

    def _handle_collisions(self):
        for hittable in self._hittable_objects:
            hits = self.ball.hits(hittable)
            for direction, delta in hits.items():
                self.ball.position = self.ball.position + direction.value * -delta
                if direction.is_horizontal:
                    self.ball.speed.y *= -1
                if direction.is_vertical:
                    self.ball.speed.x *= -1

    def move_paddle(self, paddle: int, direction: Direction | None):
        assert direction.is_vertical, "Direction must be vertical"
        if direction is None:
            self.paddles[paddle].speed = Vector2(0, 0)
        else:
            self.paddles[paddle].speed = direction.value * self.size.y * self.config.paddle_speed_ratio
    
    def stop_paddle(self, paddle: int):
        self.move_paddle(paddle, None)
    