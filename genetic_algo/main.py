from genetic_algo.classes.genetic_algorithm import GeneticAlgorithm
from genetic_algo.classes.input_params import InputParams


def main():
    input_params = InputParams('')
    genetic_algo = GeneticAlgorithm(input_params=input_params)
    genetic_algo.run()


if __name__ == '__main__':
    main()
