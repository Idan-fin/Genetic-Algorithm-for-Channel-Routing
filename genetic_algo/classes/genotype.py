from typing import List


class Genotype:

    def __init__(self, num_of_row: int, pins_position: List[List[int]]):

        # TODO: decide if grid should be List[List[List[int]]] or List[List[List[Nucleotide]]]
        self.grid = self._generate_initial_genotype(num_of_row=num_of_row, pins_position=pins_position)

    def _generate_initial_genotype(self, num_of_row: int, pins_position: List[List[int]]) -> List[List[List[int]]]:
        pass
