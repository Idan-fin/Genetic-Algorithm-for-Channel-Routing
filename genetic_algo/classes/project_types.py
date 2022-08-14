from dataclasses import dataclass


@dataclass
class Point2D:
    x: int
    y: int


@dataclass
class Nucleotide:
    x: int
    y: int
    z: int

    value: int


class Pin(Nucleotide):
    def __init__(self, *args, **kwargs):
        super(Pin).__init__(*args, **kwargs)

        self._validate()

    def _validate(self):
        assert self.value < 0
