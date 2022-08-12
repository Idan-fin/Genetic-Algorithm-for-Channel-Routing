from random import randrange

from genetic_algo.classes.input_params import InputParams
from genetic_algo.classes.genotype import Genotype


class RoutingSolution:

    def __init__(self, input_params: InputParams):
        self.fitness = self.calc_fitness()
        self.input_params = input_params
        self.genotype = Genotype(
            num_of_row=randrange(2 * self.input_params.expected_final_row_num,
                                 4 * self.input_params.expected_final_row_num),
            pins_position=self.input_params.pins_position)

    def _calc_net_length_opp(self) -> int:
        pass

    def _calc_net_length_acc(self) -> int:
        pass

    def _calc_via_numbers(self) -> int:
        pass

    def calc_fitness(self) -> float:
        pass

    def random_routing(self):
        pass

    def mutate(self):
        pass

    def optimize(self):
        pass
