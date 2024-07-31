from dpongpy import Vector2, logger
from dataclasses import dataclass, field
from random import Random
from enum import Enum
import math


class Direction(Enum):
    UP = Vector2(0, -1)
    DOWN = Vector2(0, 1)
    LEFT = Vector2(-1, 0)
    RIGHT = Vector2(1, 0)

    def __repr__(self):
        return f'<{type(self).__name__}.{self.name}>'

    def __str__(self):
        return repr(self)[1:-1]

    @property
    def is_vertical(self) -> bool:
        return self.value.x == 0
    
    @property
    def is_horizontal(self) -> bool:
        return self.value.y == 0


@dataclass
class Rectangle:
    top_left: Vector2
    bottom_right: Vector2

    def __post_init__(self):
        fst, snd = Vector2(self.top_left), Vector2(self.bottom_right)
        self.top_left = Vector2(min(fst.x, snd.x), min(fst.y, snd.y))
        self.bottom_right = Vector2(max(fst.x, snd.x), max(fst.y, snd.y))

    @property
    def top(self) -> float:
        return self.top_left.y

    @property
    def bottom(self) -> float:
        return self.bottom_right.y

    @property
    def left(self) -> float:
        return self.top_left.x

    @property
    def right(self) -> float:
        return self.bottom_right.x

    @property
    def top_right(self) -> Vector2:
        return Vector2(self.bottom_right.x, self.top_left.y)
    
    @property
    def bottom_left(self) -> Vector2:
        return Vector2(self.top_left.x, self.bottom_right.y)
    
    @property
    def corners(self) -> list[Vector2]:
        return [self.top_left, self.top_right, self.bottom_right, self.bottom_left]

    @property
    def size(self) -> Vector2:
        return self.bottom_right - self.top_left
    
    @property
    def position(self) -> Vector2:
        return (self.top_left + self.bottom_right) / 2

    def overlaps(self, other: 'Rectangle') -> bool:
        return self.top_left.x <= other.bottom_right.x \
            and self.bottom_right.x >= other.top_left.x \
            and self.top_left.y <= other.bottom_right.y \
            and self.bottom_right.y >= other.top_left.y

    def is_inside(self, other) -> bool:
        return self in other
    
    def __contains__(self, other) -> bool:
        if isinstance(other, Rectangle):
            return other.top_left in self and other.bottom_right in self
        else:
            x, y = other
            return self.top_left.x <= x <= self.bottom_right.x and \
                   self.top_left.y <= y <= self.bottom_right.y
    
    def intersection_with(self, other: 'Rectangle') -> 'Rectangle':
        if self.overlaps(other):
            return Rectangle(
                Vector2(
                    max(self.top_left.x, other.top_left.x), 
                    max(self.top_left.y, other.top_left.y)
                ), 
                Vector2(
                    min(self.bottom_right.x, other.bottom_right.x), 
                    min(self.bottom_right.y, other.bottom_right.y)
                )
            )
        return None

    def hits(self, other: 'Rectangle') -> dict[Direction, float]:
        result = dict()
        intersection = self.intersection_with(other)
        if intersection is not None:
            tl, tr, br, bl = tuple([corner in self for corner in other.corners])
            if br and not(tl or tr or bl):
                result[Direction.UP] = intersection.size.y
                result[Direction.LEFT] = intersection.size.x
            elif bl and not(tr or tl or br):
                result[Direction.UP] = intersection.size.y
                result[Direction.RIGHT] = intersection.size.x
            elif tr and not(bl or br or tl):
                result[Direction.DOWN] = intersection.size.y
                result[Direction.LEFT] = intersection.size.x
            elif tl and not(br or bl or tr):
                result[Direction.DOWN] = intersection.size.y
                result[Direction.RIGHT] = intersection.size.x
            elif (tl and tr and not (bl or br)) or (self.top <= other.top <= self.bottom < other.bottom):
                result[Direction.DOWN] = intersection.size.y
            elif (bl and br and not (tl or tr)) or (other.top < self.top <= other.bottom <= self.bottom):
                result[Direction.UP] = intersection.size.y
            elif (tl and bl and not (tr or br)) or (self.left <= other.left <= self.right < other.right):
                result[Direction.RIGHT] = intersection.size.x
            elif (tr and br and not (tl or bl)) or (other.left < self.left <= other.right <= self.right):
                result[Direction.LEFT] = intersection.size.x
            else:
                raise ValueError("Invalid collision, this is likely a bug")
        return result


class GameObject:
    def __init__(self, size, position=None, speed=None, name=None):
        self.size = Vector2(size)
        self._position = Vector2(position) if position is not None else Vector2()
        self._speed = Vector2(speed) if speed is not None else Vector2()
        self.name = name or self.__class__.__name__.lower()

    def __eq__(self, other):
        return isinstance(other, type(self)) and \
            self.name == other.name and \
            self.size == other.size and \
            self.position == other.position and \
            self.speed == other.speed

    def __hash__(self):
        return hash((type(self), self.name, self.size, self.position, self.speed))

    def __repr__(self):
        return f'<{type(self).__name__}(id={id(self)}, name={self.name}, size={self.size}, position={self.position}, speed={self.speed})>'

    def __str__(self):
        return f'{self.name}#{id(self)}'

    @property
    def position(self) -> Vector2:
        return self._position

    @position.setter
    def position(self, value: Vector2):
        old = self._position
        self._position = Vector2(value)
        if old is not None and old != self._position:
            logger.debug(f"{self} moves: {old} -> {self._position}")

    @property
    def speed(self) -> Vector2:
        return self._speed

    @speed.setter
    def speed(self, value: Vector2):
        old = self._speed
        self._speed = Vector2(value)
        if old is not None and old != self._speed:
            logger.debug(f"{self} accelerates: {old} -> {self._speed}")

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
        borders[Direction.UP] = Rectangle((-self.size.x, 0), (self.size.x * 2, -self.size.y))
        borders[Direction.DOWN] = Rectangle((-self.size.x, self.size.y), (self.size.x * 2, self.size.y * 2))
        borders[Direction.LEFT] = Rectangle((0, -self.size.y), (-self.size.x, self.size.y * 2))
        borders[Direction.RIGHT] = Rectangle((self.size.x, -self.size.y), (self.size.x * 2, self.size.y * 2))
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
                logger.debug(f"{self.ball} hits {hittable} in direction {direction.name}, overlap is {delta}")
                if delta > 0.0:
                    self.ball.position = self.ball.position + direction.value * -delta
                    if direction.is_horizontal:
                        self.ball.speed = Vector2(-self.ball.speed.x, self.ball.speed.y)
                    if direction.is_vertical:
                        self.ball.speed = Vector2(self.ball.speed.x, -self.ball.speed.y)

    def move_paddle(self, paddle: int, direction: Direction | None):
        assert direction.is_vertical, "Direction must be vertical"
        if direction is None:
            self.paddles[paddle].speed = Vector2(0, 0)
        else:
            self.paddles[paddle].speed = direction.value * self.size.y * self.config.paddle_speed_ratio
    
    def stop_paddle(self, paddle: int):
        self.move_paddle(paddle, None)
    