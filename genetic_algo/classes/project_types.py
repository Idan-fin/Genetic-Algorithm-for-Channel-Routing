from dataclasses import dataclass


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
        super(Pin).__init__(*args, **kwargs)

        self._validate()

    def _validate(self):
        assert self.value < 0
