from __future__ import annotations
from dataclasses import dataclass, field
import math
from typing import Protocol, Generator, Any


class ShapeProtocol(Protocol):
    def points(self) -> Generator[Point, Any, None]:
        ...


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def distance_to(self, other_p: Point) -> int:
        return math.floor(
            math.sqrt((other_p.x - self.x) ** 2 + (other_p.y - self.y) ** 2)
        )


@dataclass(frozen=True)
class Line:
    p1: Point
    p2: Point

    @property
    def m(self) -> float:
        dy = self.p1.y - self.p2.y
        dx = self.p1.x - self.p2.x
        return float("inf") if dx == 0 else dy / dx

    @property
    def b(self) -> float:
        return self.p1.y - (self.m * self.p1.x)

    def f(self, x: float) -> float:
        return (self.m * x) + self.b

    def g(self, y: float) -> float:
        return (y - self.b) / self.m

    @property
    def is_vertical(self) -> bool:
        return self.m == float("inf")

    @property
    def is_horizontally_compressed(self) -> bool:
        return -1.0 <= self.m <= 1.0

    def points(self):
        min_x = min(self.p1.x, self.p2.x)
        max_x = max(self.p1.x, self.p2.x)
        min_y = min(self.p1.y, self.p2.y)
        max_y = max(self.p1.y, self.p2.y)

        if self.is_vertical:
            for y in range(min_y, max_y + 1):
                yield Point(self.p1.x, y)
        else:
            if self.is_horizontally_compressed:
                for x in range(min_x, max_x + 1):
                    yield Point(x, math.floor(self.f(x)))
            else:
                for y in range(min_y, max_y + 1):
                    yield Point(math.floor(self.g(y)), y)


@dataclass
class Rectangle:
    p1: Point
    p2: Point
    sides: tuple[Line, Line, Line, Line] = field(init=False)
    top: Line = field(init=False)
    bottom: Line = field(init=False)
    left: Line = field(init=False)
    right: Line = field(init=False)

    def __post_init__(self):
        min_x = min(self.p1.x, self.p2.x)
        min_y = min(self.p1.y, self.p2.y)
        max_x = max(self.p1.x, self.p2.x)
        max_y = max(self.p1.y, self.p2.y)

        tl = Point(min_x, min_y)
        tr = Point(max_x, min_y)
        bl = Point(min_x, max_y)
        br = Point(max_x, max_y)

        self.top = Line(tl, tr)
        self.bottom = Line(bl, br)
        self.left = Line(tl, bl)
        self.right = Line(tr, br)
        self.sides = (self.top, self.bottom, self.left, self.right)

    def points(self) -> Generator[Point, Any, None]:
        for line in self.sides:
            for point in line.points():
                yield point
