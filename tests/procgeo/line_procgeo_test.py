import abc
import unittest

from tests.utils.test_utils import repeat
from procedural.procgeo import ProcGeo

REPEAT = 300


class ALineProcGeoTest(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_settings(self):
        return None, None, None

    def setUp(self):
        settings = self.get_settings()
        print("\nRunning test %s for bounds size %s" % (self.__class__.__name__, settings))
        self.cud = ProcGeo(*settings)

    @repeat(REPEAT)
    def test__get_random_line__should_work_for_same_angle(self):
        self.cud.get_random_line(1, 1, False)

    @repeat(REPEAT)
    def test__get_random_line__should_work_for_0_90_angle(self):
        self.cud.get_random_line(0, 90, False)

    @repeat(REPEAT)
    def test__get_random_line__should_work_for_0_180_angle(self):
        self.cud.get_random_line(0, 180, False)

    @repeat(REPEAT)
    def test__get_random_line__should_work_for_0_360_angle(self):
        self.cud.get_random_line(0, 360, False)


class ProcGeoTest500(ALineProcGeoTest, unittest.TestCase):

    def get_settings(self):
        return (500, 500), 10, 1


class ProcGeoTest28(ALineProcGeoTest, unittest.TestCase):

    def get_settings(self):
        return (28, 28), 2, 0


if __name__ == '__main__':
    unittest.main()
