from genetic_algo.classes.genetic_algorithm import GeneticAlgorithm
from genetic_algo.classes.input_params import InputParams
from genetic_algo.classes.output_resolver import OutputResolver
from random import seed


def print_colored_2d_list(lst):
    # define a list of colors to use for the numbers
    colors = ['\033[1;31m', '\033[1;32m', '\033[1;33m', '\033[1;34m', '\033[1;35m', '\033[1;36m']

    # iterate through the rows of the list
    for row in lst:
        # iterate through the numbers in the row
        for num in row:
            # choose a color for the number based on its value
            color = colors[abs(num) % len(colors)]
            # print the number with the chosen color
            print(f"{color}{abs(num)}\033[0m", end=' ')
        # move to the next line after printing the row
        print()


def main():
    # seed(13)
    print("start")
    input_params = InputParams('test4.json')
    genetic_algo = GeneticAlgorithm(input_params=input_params)
    result = genetic_algo.run()
    OutputResolver(result, "out.json").resolve_output()
    print("end")
    print("layer1:")
    print_colored_2d_list(result.best_solution.genotype.grid[0])
    print("layer2:")
    print_colored_2d_list(result.best_solution.genotype.grid[1])


if __name__ == '__main__':
    main()
