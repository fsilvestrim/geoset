import abc
import unittest

from geoset.tests.utils.test_utils import repeat
from geoset.procedural import ProcGeo

REPEAT = 300


class ARectProcGeoTest(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_settings(self):
        return None, None, None

    def setUp(self):
        settings = self.get_settings()
        print("\nRunning test %s for bounds size %s" % (self.__class__.__name__, settings))
        self.cud = ProcGeo(*settings)

    @repeat(REPEAT)
    def test__get_random_rect(self):
        self.cud.get_random_rect(False)


class ProcGeoTest500(ARectProcGeoTest, unittest.TestCase):

    def get_settings(self):
        return (500, 500), 10, 1


class ProcGeoTest28(ARectProcGeoTest, unittest.TestCase):

    def get_settings(self):
        return (28, 28), 2, 0


if __name__ == '__main__':
    unittest.main()
