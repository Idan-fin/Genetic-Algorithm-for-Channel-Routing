from typing import List


class InputParams:

    def __init__(self, input_file_path: str):
        self.input_file_path = input_file_path
        self.pins_position = List[List[int]]
        self.population_size: int
        self.net_length_factor: float
        self.via_numbers_factor: float
        self.max_descendants: int
        self.max_generations: int
        self.mut_1_prob: float
        self.mut_2_prob: float
        self.mut_3_prob: float
        self.mut_4_prob: float
        self.expected_final_row_num: int

    def parse_input_file(self):
        pass
