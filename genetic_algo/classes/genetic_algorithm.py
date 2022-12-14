from genetic_algo.classes.input_params import InputParams
from genetic_algo.classes.population import Population
from genetic_algo.classes.output_resolver import OutputType


class GeneticAlgorithm:
    def __init__(self, input_params: InputParams):
        self.input_params: InputParams = input_params
        self.population = Population(input_params=input_params)

    def run(self) -> OutputType:
        for i in range(self.input_params.max_generations):
            print(f"gen: {i}")
            self.population.generate_next_generation()
            self.population.reduction()
            self.population.best_solution = self.population.get_best()
            self.population.mutate_all_solutions_and_calc_new_fitness()

        self.population.optimize_best_solution()
        return OutputType(self.population.best_solution)

