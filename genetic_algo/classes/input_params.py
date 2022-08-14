from typing import List
import json


class InputParams:

    def __init__(self, input_file_path: str):
        self.input_file_path = input_file_path

        self.pins_position: List[List[int]]
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

        self._parse_input_file()

    def _parse_input_file(self):
        f = open(self.input_file_path)
        data = json.load(f)
        details = data["details"][0]
        self.population_size = details["population_size"]
        self.net_length_factor = details["fitness_params"]["net_length_factor"]
        self.via_numbers_factor = details["fitness_params"]["via_numbers_factor"]
        self.max_descendants = details["max_descendants"]
        self.max_generations = details["max_generations"]
        self.mut_1_prob = details["mut_prob"]["mut_1_prob"]
        self.mut_2_prob = details["mut_prob"]["mut_2_prob"]
        self.mut_3_prob = details["mut_prob"]["mut_3_prob"]
        self.mut_4_prob = details["mut_prob"]["mut_4_prob"]
        self.expected_final_row_num = details["expected_final_row_num"]
        self.pins_position = details["pins_position"]
        f.close()
        self._check_probability_boundary(details["mut_prob"])
        self._check_pins_position()

    @staticmethod
    def _check_probability_boundary(prob_list: list[int]):
        for prob in prob_list:
            if prob_list[prob] < 0 or prob_list[prob] > 1:
                raise ValueError("probability out of boundary")
    pass

    def _check_pins_position(self):
        if len(self.pins_position) != 2 or len(self.pins_position[0]) != len(self.pins_position[1]):
            raise ValueError("error in pins_position list size")
        match_pins: dict = {}
        for row in self.pins_position:
            for pin in row:
                if pin < 0:
                    raise ValueError("negative pin net number")
                if pin in match_pins:
                    match_pins[pin] = match_pins[pin]+1
                else:
                    match_pins[pin] = 1

        for net_number in match_pins:
            if match_pins[net_number] == 1:
                raise ValueError("net number:" + str(net_number) + " has only 1 pin")

