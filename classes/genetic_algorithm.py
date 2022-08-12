from input_params import InputParams
from population import Population


class GeneticAlgorithm:
    def __init__(self, input_params: InputParams):
        self.input_params: InputParams = input_params
        self.population = Population(input_params=input_params)

    def run(self):
        pass
