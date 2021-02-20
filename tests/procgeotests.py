import abc
import unittest

from tests.test_utils import repeat
from utils.procgeo import ProcGeo


class AProcGeoTest(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_settings(self):
        return

    def setUp(self):
        settings = self.get_settings()
        print("\nRunning test %s for bounds size %s" % (self.__class__.__name__, settings))
        self.cud = ProcGeo(*settings)

    @repeat(100)
    def test_get_random_line_should_work_for_same_angle(self):
        self.cud.get_random_line(1, 1, False)

    @repeat(100)
    def test_get_random_line_should_work_for_0_90_angle(self):
        self.cud.get_random_line(0, 90, False)

    @repeat(100)
    def test_get_random_line_should_work_for_0_180_angle(self):
        self.cud.get_random_line(0, 180, False)

    @repeat(100)
    def test_get_random_line_should_work_for_0_360_angle(self):
        self.cud.get_random_line(0, 360, False)


class ProcGeoTest500(AProcGeoTest, unittest.TestCase):

    def get_settings(self):
        return (500, 500), 10, 1


class ProcGeoTest28(AProcGeoTest, unittest.TestCase):

    def get_settings(self):
        return (28, 28), 2, 0


if __name__ == '__main__':
    unittest.main()
