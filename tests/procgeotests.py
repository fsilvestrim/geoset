import abc
import unittest
import numpy as np

from tests.test_utils import repeat
from utils.procgeo import ProcGeo
from parameterized import parameterized


class AProcGeoTest(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_settings(self):
        return

    def setUp(self):
        settings = self.get_settings()
        print("\nRunning test %s for bounds size %s" % (self.__class__.__name__, settings))
        self.cud = ProcGeo(*settings)

    @repeat(100)
    def test__get_random_line__should_work_for_same_angle(self):
        self.cud.get_random_line(1, 1, False)

    @repeat(100)
    def test__get_random_line__should_work_for_0_90_angle(self):
        self.cud.get_random_line(0, 90, False)

    @repeat(100)
    def test__get_random_line__should_work_for_0_180_angle(self):
        self.cud.get_random_line(0, 180, False)

    @repeat(100)
    def test__get_random_line__should_work_for_0_360_angle(self):
        self.cud.get_random_line(0, 360, False)

    @unittest.expectedFailure
    def test__get_random_open_triangles__should_fail_for_diff_angle_less_than_min(self):
        self.cud.get_random_open_triangles(0, 3, 3, False)

    @repeat(100)
    def test__get_random_open_triangles__should_work_for_0_90_angle(self):
        self.cud.get_random_open_triangles(0, 90, 10, False)


class ProcGeoTest500(AProcGeoTest, unittest.TestCase):

    def get_settings(self):
        return (500, 500), 10, 1


class ProcGeoTest28(AProcGeoTest, unittest.TestCase):

    def get_settings(self):
        return (28, 28), 2, 0


class ProcGeoTestUtils(unittest.TestCase):

    @parameterized.expand([
        [0,     0,  200, 0,     200],  # 0
        [2,     0,  200, 0,     198],  # 1
        [2,     2,  198, 2,     196],  # 2
        [20,    0,  200, 0,     180],  # 3
        [180,   0,  200, 0,     20],   # 4
        [180,   1,  198, 1,     18],   # 5
        [100,   0,  200, 0,     100],  # 6
        [-20,   0,  200, 20,    200],  # 7
        [-20,   2,  198, 22,    198],  # 8
        [-180,  0,  200, 180,   200],  # 9
        [497,   1,  499, 1,     2],    # 10
        [2,     1,  9,   1,     7],    # 11
    ])
    def test__get_min_max_bounds(self, val, minimum, maximum, expected_min, expected_max):
        boundaries = ProcGeo.get_min_max_bounds(val, minimum, maximum)
        self.assertEqual(expected_min, boundaries[0], "MIN - val:%i, min:%i, max:%i" % (val, minimum, maximum))
        self.assertEqual(expected_max, boundaries[1], "MAX - val:%i, min:%i, max:%i" % (val, minimum, maximum))

    @parameterized.expand([
        [0,     1,      0],  # 0
        [45,    1,      1],  # 1
        [90,    0,      1],  # 2
        [135,  -1,      1],  # 3
        [180,  -1,      0],  # 4
        [225,  -1,     -1],  # 5
        [270,   0,     -1],  # 6
        [315,   1,     -1],  # 7
        [360,   1,      0],  # 8
        [360.1, 1,      0],  # 9
    ])
    def test__get_square_unit_projection(self, angle_degrees, expected_projection_x, expected_projection_y):
        projections = ProcGeo.get_square_unit_projection(angle_degrees)
        self.assertAlmostEqual(expected_projection_x, projections[0], delta=0.01, msg="X - angle:%i" % angle_degrees)
        self.assertAlmostEqual(expected_projection_y, projections[1], delta=0.01, msg="Y - angle:%i" % angle_degrees)


if __name__ == '__main__':
    unittest.main()
