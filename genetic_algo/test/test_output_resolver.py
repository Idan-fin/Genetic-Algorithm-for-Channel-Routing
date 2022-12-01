import unittest
from genetic_algo.classes.routing_solution import RoutingSolution
from genetic_algo.classes.output_resolver import OutputResolver, OutputType
from genetic_algo.classes.input_params import InputParams


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

    def test_generate_next_generation_sanity_check(self):
        resolver = OutputResolver(OutputType(self._get_simple_routing_example()), "test_out.json")
        resolver.resolve_output()

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
