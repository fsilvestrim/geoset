import abc
import unittest

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


if __name__ == '__main__':
    unittest.main()
