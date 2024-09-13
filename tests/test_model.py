import unittest
from dpongpy.model import *
import math


class TestDirection(unittest.TestCase):
    def test_is_vertical(self):
        self.assertTrue(Direction.UP.is_vertical)
        self.assertTrue(Direction.DOWN.is_vertical)
        self.assertFalse(Direction.LEFT.is_vertical)
        self.assertFalse(Direction.RIGHT.is_vertical)

    def test_is_horizontal(self):
        self.assertTrue(Direction.LEFT.is_horizontal)
        self.assertTrue(Direction.RIGHT.is_horizontal)
        self.assertFalse(Direction.UP.is_horizontal)
        self.assertFalse(Direction.DOWN.is_horizontal)


class TestRectangle(unittest.TestCase):
    @staticmethod
    def rect(tl=None, position=None, size=(1, 1)):
        size = Vector2(size)
        if tl is not None:
            tl = Vector2(tl)
            return Rectangle(tl, tl + size)
        if position is not None:
            position = Vector2(position)
            return Rectangle(position - size / 2, position + size / 2)
        raise ValueError("tl or center must be provided")
    
    def indexes(self, rows = 3, cols = 3, include_center=True):
        for i in range(rows):
            for j in range(cols):
                if not include_center and i == (rows // 2) and j == (cols // 2):
                    continue
                yield i, j

    def setUp(self) -> None:
        self.rectangles = dict()
        for i, j in self.indexes():
            self.rectangles[(i, j)] = self.rect(tl=(j, i))
        self.rectangles[(1, 1)] = self.rect(position=(1.5, 1.5), size=(2, 2))
        self.box = self.rect(tl=(0, 0), size=(3, 3))
        self.other = self.rect(tl=(4, 4))

    def all_rectangles(self):
        return list(self.rectangles.values()) + [self.box, self.other]

    def test_create_from_wrong_args(self):
        rect = Rectangle((0, 0), (10, -10))
        self.assertEqual(rect.top_left, Vector2(0, -10))
        self.assertEqual(rect.bottom_right, Vector2(10, 0))

    def test_properties(self):
        for i, j in self.indexes():
            with self.subTest(rect=f'in position {i}, {j}'):
                rect = self.rectangles[(i, j)]
                if i == 1 and j == 1:
                    self.assertEqual(rect.top_left, Vector2(j - 0.5, i - 0.5))
                    self.assertEqual(rect.bottom_right, Vector2(j + 1.5, i + 1.5))
                    self.assertEqual(rect.position, Vector2(j + 0.5, i + 0.5))
                    self.assertEqual(rect.size, Vector2(2, 2))
                else:
                    self.assertEqual(rect.top_left, Vector2(j, i))
                    self.assertEqual(rect.bottom_right, Vector2(j + 1, i + 1))
                    self.assertEqual(rect.position, Vector2(j + 0.5, i + 0.5))
                    self.assertEqual(rect.size, Vector2(1, 1))
        with self.subTest(rect=f'box'):
            self.assertEqual(self.box.top_left, Vector2(0, 0))
            self.assertEqual(self.box.bottom_right, Vector2(3, 3))
            self.assertEqual(self.box.position, Vector2(1.5, 1.5))
            self.assertEqual(self.box.size, Vector2(3, 3))
        with self.subTest(rect=f'other'):
            self.assertEqual(self.other.top_left, Vector2(4, 4))
            self.assertEqual(self.other.bottom_right, Vector2(5, 5))
            self.assertEqual(self.other.position, Vector2(4.5, 4.5))
            self.assertEqual(self.other.size, Vector2(1, 1))

    def test_overlap(self):
        center = self.rectangles[(1, 1)]
        for i, j in self.indexes(include_center=False):
            with self.subTest(rect=f'in position {i}, {j}', overlaps='center'):
                self.assertTrue(self.rectangles[(i, j)].overlaps(center))
            with self.subTest(rect=f'center', overlaps=f'rect in position {i}, {j}'):
                self.assertTrue(center.overlaps(self.rectangles[(i, j)]))

    def test_overlap_implies_is_inside(self):
        for i, j in self.indexes(include_center=False):
            with self.subTest(rect=f'in position {i}, {j}', overlaps='box'):
                self.assertTrue(self.rectangles[(i, j)].overlaps(self.box))
            with self.subTest(rect=f'box', overlaps=f'rect in position {i}, {j}'):
                self.assertTrue(self.box.overlaps(self.rectangles[(i, j)]))

    def test_not_overlap(self):
        for i, j in self.indexes():
            for y, x in self.indexes():
                if abs(i - y) > 1 or abs(j - x) > 1:
                    with self.subTest(rect=f'in position {i}, {j}', doesnt_overlap=f'position {y}, {x}'):
                        self.assertFalse(self.rectangles[(i, j)].overlaps(self.rectangles[(y, x)]))
            with self.subTest(rect=f'in position {i}, {j}', doesnt_overlap='other'):
                self.assertFalse(self.rectangles[(i, j)].overlaps(self.other))
    
    def test_wall_is_overlap(self):
        for i, j in self.indexes(include_center=False):
            for y, x in self.indexes(include_center=False):
                if abs(i - y) + abs(j - x) == 1:
                    with self.subTest(rect=f'in position {i}, {j}', overlaps=f'position {y}, {x}'):
                        self.assertTrue(self.rectangles[(i, j)].overlaps(self.rectangles[(y, x)]))

    def test_is_inside(self):
        for i, j in self.indexes():
            with self.subTest(rect=f'in position {i}, {j}', is_inside='box'):
                self.assertTrue(self.rectangles[(i, j)].is_inside(self.box))
                self.assertIn(self.rectangles[(i, j)], self.box)
            
    def test_is_not_inside(self):
        for i, j in self.indexes():
            with self.subTest(rect=f'box', is_not_inside=f'rect in position {i}, {j}'):
                self.assertFalse(self.box.is_inside(self.rectangles[(i, j)]))
                self.assertNotIn(self.box, self.rectangles[(i, j)])
        with self.subTest(rect=f'box', is_not_inside=f'other'):
            self.assertFalse(self.box.is_inside(self.other))
            self.assertNotIn(self.box, self.other)
        with self.subTest(rect=f'other', is_not_inside=f'box'):
            self.assertFalse(self.other.is_inside(self.box))
            self.assertNotIn(self.other, self.box)

    def test_intersection(self):
        center = self.rectangles[(1, 1)]
        def test_intersection(i, j, tl, size):
            with self.subTest(rect='center', intersection=f'rect in position {i}, {j}'):
                rect = self.rectangles[(i, j)]
                expected = self.rect(tl=tl, size=size)
                self.assertEqual(center.intersection_with(rect), expected)
                self.assertEqual(rect.intersection_with(center), expected)
                self.assertIsNone(rect.intersection_with(self.other))
        test_intersection(0, 0, (0.5, 0.5), (0.5, 0.5))
        test_intersection(1, 0, (0.5, 1), (0.5, 1))
        test_intersection(2, 0, (0.5, 2), (0.5, 0.5))
        test_intersection(0, 1, (1, 0.5), (1, 0.5))
        test_intersection(2, 1, (1, 2), (1, 0.5))
        test_intersection(0, 2, (2, 0.5), (0.5, 0.5))
        test_intersection(1, 2, (2, 1), (0.5, 1))
        test_intersection(2, 2, (2, 2), (0.5, 0.5))
        
    def test_intersection_with_self(self):
        for i, j in self.indexes():
            with self.subTest(rect=f'in position {i}, {j}'):
                rect = self.rectangles[(i, j)]
                self.assertEqual(rect.intersection_with(rect), rect)

    def test_intersection_with_non_overlapping(self):
        for i, j in self.indexes():
            with self.subTest(rect=f'in position {i}, {j}'):
                rect = self.rectangles[(i, j)]
                self.assertIsNone(rect.intersection_with(self.other))
                self.assertIsNone(self.other.intersection_with(rect))

    def test_intersection_with_inside(self):
        for i, j in self.indexes():
            with self.subTest(rect=f'in position {i}, {j}'):
                rect = self.rectangles[(i, j)]
                self.assertEqual(rect.intersection_with(self.box), rect)
                self.assertEqual(self.box.intersection_with(rect), rect)
    
    def test_hits_bigger_with_smaller(self):
        center = self.rectangles[(1, 1)]
        with self.subTest(rect='center', hits=f'rect in position {0}, {0}'):
            hits = center.hits(self.rectangles[(0, 0)])
            self.assertEqual(hits, {Direction.LEFT: 0.5, Direction.UP: 0.5})
        with self.subTest(rect='center', hits=f'rect in position {0}, {1}'):
            hits = center.hits(self.rectangles[(0, 1)])
            self.assertEqual(hits, {Direction.UP: 0.5})
        with self.subTest(rect='center', hits=f'rect in position {0}, {2}'):
            hits = center.hits(self.rectangles[(0, 2)])
            self.assertEqual(hits, {Direction.UP: 0.5, Direction.RIGHT: 0.5})
        with self.subTest(rect='center', hits=f'rect in position {1}, {0}'):
            hits = center.hits(self.rectangles[(1, 0)])
            self.assertEqual(hits, {Direction.LEFT: 0.5})
        with self.subTest(rect='center', hits=f'rect in position {1}, {2}'):
            hits = center.hits(self.rectangles[(1, 2)])
            self.assertEqual(hits, {Direction.RIGHT: 0.5})
        with self.subTest(rect='center', hits=f'rect in position {2}, {0}'):
            hits = center.hits(self.rectangles[(2, 0)])
            self.assertEqual(hits, {Direction.LEFT: 0.5, Direction.DOWN: 0.5})
        with self.subTest(rect='center', hits=f'rect in position {2}, {1}'):
            hits = center.hits(self.rectangles[(2, 1)])
            self.assertEqual(hits, {Direction.DOWN: 0.5})
        with self.subTest(rect='center', hits=f'rect in position {2}, {2}'):
            hits = center.hits(self.rectangles[(2, 2)])
            self.assertEqual(hits, {Direction.DOWN: 0.5, Direction.RIGHT: 0.5})

    def test_hits_smaller_with_bigger(self):
        center = self.rectangles[(1, 1)]
        with self.subTest(rect=f'in position {0}, {0}', hits='center'):
            hits = self.rectangles[(0, 0)].hits(center)
            self.assertEqual(hits, {Direction.RIGHT: 0.5, Direction.DOWN: 0.5})
        with self.subTest(rect=f'in position {0}, {1}', hits='center'):
            hits = self.rectangles[(0, 1)].hits(center)
            self.assertEqual(hits, {Direction.DOWN: 0.5})
        with self.subTest(rect=f'in position {0}, {2}', hits='center'):
            hits = self.rectangles[(0, 2)].hits(center)
            self.assertEqual(hits, {Direction.DOWN: 0.5, Direction.LEFT: 0.5})
        with self.subTest(rect=f'in position {1}, {0}', hits='center'):
            hits = self.rectangles[(1, 0)].hits(center)
            self.assertEqual(hits, {Direction.RIGHT: 0.5})
        with self.subTest(rect=f'in position {1}, {2}', hits='center'):
            hits = self.rectangles[(1, 2)].hits(center)
            self.assertEqual(hits, {Direction.LEFT: 0.5})
        with self.subTest(rect=f'in position {2}, {0}', hits='center'):
            hits = self.rectangles[(2, 0)].hits(center)
            self.assertEqual(hits, {Direction.RIGHT: 0.5, Direction.UP: 0.5})
        with self.subTest(rect=f'in position {2}, {1}', hits='center'):
            hits = self.rectangles[(2, 1)].hits(center)
            self.assertEqual(hits, {Direction.UP: 0.5})
        with self.subTest(rect=f'in position {2}, {2}', hits='center'):
            hits = self.rectangles[(2, 2)].hits(center)
            self.assertEqual(hits, {Direction.UP: 0.5, Direction.LEFT: 0.5})
    
    def test_not_hits(self):
        center = self.rectangles[(1, 1)]
        with self.subTest(rect='center', doesnt_hit=f'other'):
            hits = center.hits(self.other)
            self.assertEqual(hits, {})
    

class TestPong(unittest.TestCase):
    def setUp(self) -> None:
        self.size = Vector2(160, 90)
        self.pong = Pong(size=self.size)
        self.paddle_ratio=Vector2(0.1, 0.01)
        self.ball_ratio=0.05
        self.ball_speed_ratio=0.1
        self.paddle_speed_ratio=0.05
        self.paddle_padding=0.05
        self.expected_config = Config(
            self.paddle_ratio,
            self.ball_ratio,
            self.ball_speed_ratio,
            self.paddle_speed_ratio,
            self.paddle_padding,
        )
        self.min_dim = min(*self.size)

    def test_initial_config(self):
        self.assertEqual(
            self.pong.config, 
            self.expected_config
        )

    def test_two_paddles(self):
        self.assertEqual(len(self.pong.paddles), 2)

    def test_paddle_size(self):
        self.assertEqual(self.pong.size, self.size)

    def test_ball_position_is_initially_centered(self):
        self.assertEqual(self.pong.ball.position, self.size / 2)

    def test_ball_size_is_proportional_to_window_size(self):
        self.assertEqual(self.pong.ball.size, Vector2(self.min_dim * self.ball_ratio))

    def test_ball_speed_is_proportional_to_windows_size_and_random_direction(self):
        ball_speed_modulus, ball_speed_angle = self.pong.ball.speed.as_polar()
        self.assertAlmostEqual(ball_speed_modulus, self.ball_speed_ratio * self.min_dim)
        self.assertGreaterEqual(ball_speed_angle, 0)
        self.assertLessEqual(ball_speed_angle, 2 * math.pi)

    def test_paddle_size_is_proportional_to_window_size(self):
        for paddle in self.pong.paddles:
            self.assertEqual(paddle.size, Vector2(self.size.elementwise() * self.paddle_ratio))

    def test_paddle_position_is_initially_centered_vertically(self):
        for paddle in self.pong.paddles:
            self.assertEqual(paddle.position.y, self.size.y / 2)
        padding = self.paddle_padding * self.size.x + (self.size.elementwise() * self.paddle_ratio).x / 2
        self.assertEqual(self.pong.paddles[0].position.x, padding)
        self.assertEqual(self.pong.paddles[1].position.x, self.size.x - padding)

    def test_update(self):
        self.pong.move_paddle(1, Direction.DOWN)
        self.pong.move_paddle(0, Direction.UP)
        initial_positions = {
            'ball': self.pong.ball.position,
            'paddles': [paddle.position for paddle in self.pong.paddles]
        }
        speeds = {
            'ball': self.pong.ball.speed,
            'paddles': [paddle.speed for paddle in self.pong.paddles]
        }
        dt = 2
        self.pong.update(dt)
        with self.subTest(obj='ball', initial_pos=initial_positions['ball'], speed=speeds['ball']):
            self.assertEqual(self.pong.ball.position, initial_positions['ball'] + dt * speeds['ball'])
        for i, paddle in enumerate(self.pong.paddles):
            with self.subTest(obj=f'paddle {i}', initial_pos=initial_positions['paddles'][i], speed=speeds['paddles'][i]):
                self.assertEqual(paddle.position, initial_positions['paddles'][i] + dt * speeds['paddles'][i])

    def test_hit_top_wall(self):
        ball = self.pong.ball
        ball.position = Vector2(self.size.x / 2, 1)
        wall = self.pong.board.walls[Direction.UP]
        self.assertEqual(ball.hits(wall), {Direction.UP: 1.25})

    def test_hit_bottom_wall(self):
        ball = self.pong.ball
        ball.position = Vector2(self.size.x / 2, self.size.y - 1)
        wall = self.pong.board.walls[Direction.DOWN]
        self.assertEqual(ball.hits(wall), {Direction.DOWN: 1.25})

    def test_hit_left_paddle(self):
        ball = self.pong.ball
        paddle = self.pong.paddles[0]
        ball.position = paddle.position + Vector2(paddle.size.x / 2, 0)
        self.assertEqual(ball.hits(paddle), {Direction.LEFT: 2.25})

    def test_hit_right_paddle(self):
        ball = self.pong.ball
        paddle = self.pong.paddles[1]
        ball.position = paddle.position - Vector2(paddle.size.x / 2, 0)
        self.assertEqual(ball.hits(paddle), {Direction.RIGHT: 2.25})

    def _test_collisions(self, direction: Direction, delta: float = 1, max_rounds=None):
        def log(i):
            print(f"Step {i}: position={self.pong.ball.position}, speed={self.pong.ball.speed}")
        if max_rounds is None:
            max_rounds = int(max(*self.size) // delta)
        self.pong.ball.speed = direction.value
        for i in range(max_rounds + 1):
            log(i)
            self.pong.update(delta)
            if self.pong.ball.speed != direction.value:
                break
        log(i + 1)
        with self.subTest(direction=direction.name, rounds=i, max_rounds=max_rounds):
            self.assertLess(i, max_rounds)
            self.assertNotEqual(self.pong.ball.speed, direction.value)

    def test_collision_with_top_wall(self):
        self._test_collisions(Direction.UP)

    def test_collision_with_bottom_wall(self):
        self._test_collisions(Direction.DOWN)

    def test_collision_with_left_paddle(self):
        self._test_collisions(Direction.LEFT)

    def test_collision_with_right_paddle(self):
        self._test_collisions(Direction.RIGHT)
    