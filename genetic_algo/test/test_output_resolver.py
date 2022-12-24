import unittest
from genetic_algo.classes.routing_solution import RoutingSolution
from genetic_algo.classes.output_resolver import OutputResolver, OutputType
from genetic_algo.classes.input_params import InputParams


class MyTestCase(unittest.TestCase):
    def print_colored_2d_list(self, lst):
        # define a list of colors to use for the numbers
        colors = ['\033[1;31m', '\033[1;32m', '\033[1;33m', '\033[1;34m', '\033[1;35m', '\033[1;36m']

        # iterate through the rows of the list
        for row in lst:
            # iterate through the numbers in the row
            for num in row:
                # choose a color for the number based on its value
                color = colors[num % len(colors)]
                # print the number with the chosen color
                print(f"{color}{num}\033[0m", end=' ')
            # move to the next line after printing the row
            print()

    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

    def test_generate_next_generation_sanity_check(self):
        resolver = OutputResolver(OutputType(self._get_simple_routing_example()), "test_out.json")
        resolver.resolve_output()
    def test_print(self):
        numbers = [[1, 2, 3], [4, 4, 6], [7, 8, 9]]
        self.print_colored_2d_list(numbers)

    @staticmethod
    def _get_simple_routing_example() -> RoutingSolution:
        f = open("test1.json", "w")
        test1 = """{
                    "details": [
                        {
                            "population_size": 10,
                            "fitness_params":
                            {
                                "net_length_factor": 1.001,
                                "via_numbers_factor": 2.0
                            },
                            "max_descendants": 10,
                            "max_generations": 200,
                            "mut_prob": 
                            {
                                "mut_1_prob": 0.001,
                                "mut_2_prob": 0.002,
                                "mut_3_prob": 0.003,
                                "mut_4_prob": 0.004
                            },
                            "expected_final_row_num": 20,
                            "pins_position": [[1, 2, 3], [3, 2, 1]],
                            "preferred_direction_layer": [0,1]
                        }
                    ]
                }
                """
        f.write(test1)
        f.close()
        return RoutingSolution(InputParams("test1.json"))

if __name__ == '__main__':
    unittest.main()
