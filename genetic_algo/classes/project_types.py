from dataclasses import dataclass
from enum import IntEnum


@dataclass
class Point2D:
    # TODO: change to column, row, layer
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

    def __hash__(self):
        # since we are inheriting from dataclass and it's a mutable class we need to implement __hash__

        # TODO: verify that this is a valid hash
        # -1 if last row to avoid discrepancies when extend the grid
        tuple_to_hash = (self.x, -1 if self.y else 0, self.z)
        return hash(tuple_to_hash)

    def _validate(self):
        assert self.value < 0


class Direction(IntEnum):
    horizontal = 0
    vertical = 1
