from genetic_algo.classes.input_params import InputParams
from genetic_algo.classes.population import Population
from genetic_algo.classes.output_resolver import OutputType


class GeneticAlgorithm:
    def __init__(self, input_params: InputParams):
        self.input_params: InputParams = input_params
        self.population = Population(input_params=input_params)

    def run(self) -> OutputType:
        pass
