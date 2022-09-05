import unittest
from genetic_algo.classes.genotype import Genotype
from genetic_algo.classes.project_types import Point3D


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_calculate_edge_index(self):
        g = Genotype(num_of_row=150, pins_position=[[1, 2, 3], [1, 2, 3]])
        for i in range(0, 150):
            for j in range(0, 3):
                for k in range(0, 2):
                    self.assertEqual(g.calculate_genotype_index(g._calculate_edge_index(x=i, y=j, z=k)), Point3D(i, j, k))

        pass


if __name__ == '__main__':
    unittest.main()
