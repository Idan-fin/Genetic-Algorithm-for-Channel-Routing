from dataclasses import dataclass
from enum import IntEnum


@dataclass
class Point2D:
    x: int
    y: int


@dataclass
class Point3D(Point2D):
    z: int


@dataclass
class Nucleotide(Point3D):
    value: int


class Pin(Nucleotide):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._validate()

    def _validate(self):
        assert self.value < 0


class Direction(IntEnum):
    horizontal = 0
    vertical = 1
