from typing import List


class Genotype:

    def __init__(self, num_of_row: int, pins_position: List[List[int]]):
        self.genotype = self._generate_initial_genotype(num_of_row=num_of_row, pins_position=pins_position)

    def _generate_initial_genotype(self, num_of_row: int, pins_position: List[List[int]]) -> List[List[List[int]]]:
        pass
