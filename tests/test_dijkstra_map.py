import numpy as np
import unittest

# Local modules
from dijkstra_map import dijkstra_map


class FloodTestCase(unittest.TestCase):
    def setUp(self):
        self.input_map = np.array(
            [
                [1, 1, 1, 0],
                [1, 0, 1, 1],
                [1, 0, 1, 1],
                [1, 1, 1, 1]
            ],
            dtype=int
        )

        self.walls_map = np.array(
            [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 0]
            ],
            dtype=int
        )

    def test_flooding(self):
        output_map = np.array(
            [
                [1, 1, 1, 0],
                [1, 0, 1, 1],
                [1, 0, 0, 2],
                [1, 1, 0, 3]
            ],
            dtype=int
        )
        d_map = dijkstra_map(self.input_map, self.walls_map)
        np.testing.assert_array_equal(d_map, output_map)

    def test_flooding_limit(self):
        output_map = np.array(
            [
                [1, 1, 1, 0],
                [1, 0, 1, 1],
                [1, 0, 2, 2],
                [1, 1, 2, 2]
            ],
            dtype=int
        )
        d_map = dijkstra_map(self.input_map, self.walls_map, limit=2)
        np.testing.assert_array_equal(d_map, output_map)

    def test_flooding_without_walls(self):
        output_map = np.array(
            [
                [1, 1, 1, 0],
                [1, 0, 1, 1],
                [1, 0, 1, 2],
                [1, 1, 1, 2]
            ],
            dtype=int
        )
        d_map = dijkstra_map(self.input_map)
        np.testing.assert_array_equal(d_map, output_map)


if __name__ == '__main__':
    unittest.main()
