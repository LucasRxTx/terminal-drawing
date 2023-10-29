import unittest

from shapes import Line, Point


class TestNewCommand(unittest.TestCase):
    def test_give_a_line_that_is_vertical_when_is_vertical_is_accessed_then_it_returns_true(
        self,
    ):
        vertical_lines = [
            Line(Point(0, 0), Point(0, 9)),
            Line(Point(2, 1), Point(2, 3)),
            Line(Point(99, 1), Point(99, 1000)),
        ]

        for line in vertical_lines:
            with self.subTest(line=line):
                self.assertTrue(line.is_vertical)

    def test_given_a_line_that_is_not_vertical_when_is_vertical_is_accessed_then_it_returns_false(
        self,
    ):
        vertical_lines = [
            Line(Point(0, 1), Point(1, 9)),
            Line(Point(2, 1), Point(9, 3)),
            Line(Point(99, 1), Point(97, 1000)),
        ]

        for line in vertical_lines:
            with self.subTest(line=line):
                self.assertFalse(line.is_vertical)

    def test_given_valid_new_command_then_a_new_command_is_returned(self):
        lines = [
            (
                Line(Point(0, 0), Point(10, 10)),
                {  # Identity
                    (0, 0),
                    (1, 1),
                    (2, 2),
                    (3, 3),
                    (4, 4),
                    (5, 5),
                    (6, 6),
                    (7, 7),
                    (8, 8),
                    (9, 9),
                    (10, 10),
                },
            ),
            (  # Horizontal compression
                Line(Point(0, 0), Point(5, 10)),
                {
                    (0, 0),
                    (0, 1),
                    (1, 2),
                    (1, 3),
                    (2, 4),
                    (2, 5),
                    (3, 6),
                    (3, 7),
                    (4, 8),
                    (4, 9),
                    (5, 10),
                },
            ),
            (  # Horizontal streatch
                Line(Point(0, 0), Point(10, 5)),
                {
                    (0, 0),
                    (1, 0),
                    (2, 1),
                    (3, 1),
                    (4, 2),
                    (5, 2),
                    (6, 3),
                    (7, 3),
                    (8, 4),
                    (9, 4),
                    (10, 5),
                },
            ),
            (  # Horizontal
                Line(Point(2, 5), Point(10, 5)),
                {
                    (2, 5),
                    (3, 5),
                    (4, 5),
                    (5, 5),
                    (6, 5),
                    (7, 5),
                    (8, 5),
                    (9, 5),
                    (10, 5),
                },
            ),
            (  # Vertical
                Line(Point(5, 2), Point(5, 10)),
                {
                    (5, 2),
                    (5, 3),
                    (5, 4),
                    (5, 5),
                    (5, 6),
                    (5, 7),
                    (5, 8),
                    (5, 9),
                    (5, 10),
                },
            ),
            (  # Vertical
                Line(Point(0, 9), Point(5, 0)),
                {
                    (0, 9),
                    (0, 8),
                    (1, 7),
                    (1, 6),
                    (2, 5),
                    (2, 4),
                    (3, 3),
                    (3, 2),
                    (4, 1),
                    (5, 0),
                },
            ),
        ]

        for line, expected_points in lines:
            with self.subTest(line=line):
                points = list(line.points())
                for point in points:
                    with self.subTest(point=point):
                        self.assertIn(
                            (point.x, point.y),
                            expected_points,
                            "Unexpected point in output",
                        )

                self.assertEqual(
                    len(points),
                    len(expected_points),
                    "Expected count of points to match",
                )
