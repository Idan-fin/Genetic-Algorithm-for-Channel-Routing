import unittest

from genetic_algo.classes.routing_solution import RoutingSolution
from genetic_algo.classes.input_params import InputParams


class RoutingSolutionTest(unittest.TestCase):

    def setUp(self) -> None:

        pass

    def test_fitness_func1(self):
        solution = self._get_simple_routing_example()
        self.assertAlmostEqual(1.0/solution.calc_fitness_func1(), len(solution.genotype.grid))

    def test_via_counter(self):
        solution = self._get_simple_routing_example()
        for i, y in enumerate(solution.genotype.grid):
            for j, z in enumerate(y):
                solution.genotype.grid[i][j][0] = i + 1
                solution.genotype.grid[i][j][1] = i + 1
                self.assertEqual(i * len(solution.genotype.grid[0]) + j + 1, solution._calc_via_numbers())
        for i, y in enumerate(solution.genotype.grid):
            for j, z in enumerate(y):
                solution.genotype.grid[i][j][0] = 0
                self.assertEqual(len(solution.genotype.grid) * len(solution.genotype.grid[0]) -
                                 i * len(solution.genotype.grid[0]) - j - 1, solution._calc_via_numbers())

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
