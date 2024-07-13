import unittest
from dpongpy.model import *


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
    def rect(min=None, position=None, size=(1, 1)):
        size = Vector2(size)
        if min is not None:
            min = Vector2(min)
            return Rectangle(min, min + size)
        if position is not None:
            position = Vector2(position)
            return Rectangle(position - size / 2, position + size / 2)
        raise ValueError("min or center must be provided")
    
    def indexes(self, rows = 3, cols = 3, include_center=True):
        for i in range(rows):
            for j in range(cols):
                if not include_center and i == (rows // 2) and j == (cols // 2):
                    continue
                yield i, j

    def setUp(self) -> None:
        self.rectangles = dict()
        for i, j in self.indexes():
            self.rectangles[(i, j)] = self.rect(min=(j, i))
        self.rectangles[(1, 1)] = self.rect(position=(1.5, 1.5), size=(2, 2))
        self.box = self.rect(min=(0, 0), size=(3, 3))
        self.other = self.rect(min=(4, 4))

    def all_rectangles(self):
        return list(self.rectangles.values()) + [self.box, self.other]

    def test_properties(self):
        for i, j in self.indexes():
            with self.subTest(rect=f'in position {i}, {j}'):
                rect = self.rectangles[(i, j)]
                if i == 1 and j == 1:
                    self.assertEqual(rect.min, Vector2(j - 0.5, i - 0.5))
                    self.assertEqual(rect.max, Vector2(j + 1.5, i + 1.5))
                    self.assertEqual(rect.position, Vector2(j + 0.5, i + 0.5))
                    self.assertEqual(rect.size, Vector2(2, 2))
                else:
                    self.assertEqual(rect.min, Vector2(j, i))
                    self.assertEqual(rect.max, Vector2(j + 1, i + 1))
                    self.assertEqual(rect.position, Vector2(j + 0.5, i + 0.5))
                    self.assertEqual(rect.size, Vector2(1, 1))
        with self.subTest(rect=f'box'):
            self.assertEqual(self.box.min, Vector2(0, 0))
            self.assertEqual(self.box.max, Vector2(3, 3))
            self.assertEqual(self.box.position, Vector2(1.5, 1.5))
            self.assertEqual(self.box.size, Vector2(3, 3))
        with self.subTest(rect=f'other'):
            self.assertEqual(self.other.min, Vector2(4, 4))
            self.assertEqual(self.other.max, Vector2(5, 5))
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
    
    def test_border_is_overlap(self):
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
        def test_intersection(i, j, min, size):
            with self.subTest(rect='center', intersection=f'rect in position {i}, {j}'):
                rect = self.rectangles[(i, j)]
                expected = self.rect(min=min, size=size)
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