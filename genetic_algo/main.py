from genetic_algo.classes.genetic_algorithm import GeneticAlgorithm
from genetic_algo.classes.input_params import InputParams
from genetic_algo.classes.output_resolver import OutputResolver
from random import seed

def main():
    seed(13)
    input_params = InputParams('test4.json')
    genetic_algo = GeneticAlgorithm(input_params=input_params)
    OutputResolver(genetic_algo.run(), "out.json").resolve_output()


if __name__ == '__main__':
    main()
