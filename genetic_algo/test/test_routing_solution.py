import unittest

from genetic_algo.classes.routing_solution import RoutingSolution
from genetic_algo.classes.input_params import InputParams


class RoutingSolutionTest(unittest.TestCase):

    def setUp(self) -> None:

        pass

    def test_fitness_func1(self):
        solution = self._get_simple_routing_example()
        self.assertAlmostEqual(1.0/solution.calc_fitness_func1(), len(solution.genotype.grid[0]))

    def test_via_counter(self):
        solution = self._get_simple_routing_example()
        for i, y in enumerate(solution.genotype.grid[0]):
            for j, z in enumerate(y):
                solution.genotype.grid[0][i][j] = i + 1
                solution.genotype.grid[1][i][j] = i + 1
                self.assertEqual(i * len(solution.genotype.grid[0][0]) + j + 1, solution._calc_via_numbers())
        for i, y in enumerate(solution.genotype.grid[0]):
            for j, z in enumerate(y):
                solution.genotype.grid[0][i][j] = 0
                self.assertEqual(len(solution.genotype.grid[0]) * len(solution.genotype.grid[0][0]) -
                                 i * len(solution.genotype.grid[0][0]) - j - 1, solution._calc_via_numbers())

    def test_calc_net_length_opp(self):
        solution = self._get_simple_routing_example()
        for i, y in enumerate(solution.genotype.grid[1]):
            for j, z in enumerate(y):
                if j < len(solution.genotype.grid[1][0]) and 0 < i < len(solution.genotype.grid[1]) - 1:
                    solution.genotype.grid[1][i][j] = j + 8
                    solution.genotype.grid[1][i + 1][j] = j + 8
                    self.assertEqual(0,
                                     solution._calc_net_length_opp())

        solution = self._get_simple_routing_example()
        for i, y in enumerate(solution.genotype.grid[0]):
            for j, z in enumerate(y):
                if j < len(solution.genotype.grid[0][0]) and 0 < i < len(solution.genotype.grid[0])-1:
                    solution.genotype.grid[0][i][j] = j+8
                    solution.genotype.grid[0][i+1][j] = j+8
                    self.assertEqual((i-1) * len(solution.genotype.grid[0][0]) + j + 1, solution._calc_net_length_opp())

    def test_calc_net_length_acc(self):
        solution = self._get_simple_routing_example()
        for i, y in enumerate(solution.genotype.grid[0]):
            for j, z in enumerate(y):
                if j < len(solution.genotype.grid[0][0])-1 and 0 < i < len(solution.genotype.grid[0])-1:
                    solution.genotype.grid[0][i][j] = i+8
                    solution.genotype.grid[0][i][j+1] = i+8
                    self.assertEqual((i-1) * (len(solution.genotype.grid[0][0])-1) + j + 1, solution._calc_net_length_acc())

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
