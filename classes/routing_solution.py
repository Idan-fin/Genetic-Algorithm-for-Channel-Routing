from input_params import InputParams
from genotype import Genotype
from random import randrange


class RoutingSolution:

    def __init__(self, input_params: InputParams):
        self.fitness = self.calc_fitness()
        self.input_params = input_params
        self.genotype = Genotype(num_of_row= randrange(self.input_params.expected_final_row_num),
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
