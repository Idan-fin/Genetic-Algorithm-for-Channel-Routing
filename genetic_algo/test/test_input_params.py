import unittest
from genetic_algo.classes.input_params import InputParams
import os
from genetic_algo.classes.project_types import Direction

class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
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
        pass

    def tearDown(self) -> None:
        os.remove("test1.json")
        pass

    def test_InputParams(self):
        input_param = InputParams('test1.json')
        self.assertIsNotNone(input_param)
        self.assertEqual(input_param.mut_1_prob, 0.001)
        self.assertEqual(input_param.mut_2_prob, 0.002)
        self.assertEqual(input_param.mut_3_prob, 0.003)
        self.assertEqual(input_param.mut_4_prob, 0.004)
        self.assertEqual(input_param.population_size, 10)
        self.assertEqual(input_param.net_length_factor, 1.001)
        self.assertEqual(input_param.via_numbers_factor, 2.0)
        self.assertEqual(input_param.max_descendants, 10)
        self.assertEqual(input_param.max_generations, 200)
        self.assertEqual(input_param.expected_final_row_num, 20)
        self.assertEqual(input_param.preferred_direction_layer[1], Direction.vertical)
        self.assertEqual(input_param.preferred_direction_layer[0], Direction.horizontal)

        pass


if __name__ == '__main__':
    unittest.main()
