import abc
import unittest

from geoset.tests.utils.test_utils import repeat
from geoset.procedural import ProcGeo


REPEAT = 300

class ATriangleProcGeoTest(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_settings(self):
        return

    def setUp(self):
        settings = self.get_settings()
        print("\nRunning test %s for bounds size %s" % (self.__class__.__name__, settings))
        self.cud = ProcGeo(*settings)

    @unittest.expectedFailure
    def test__get_random_open_triangles__should_fail_for_diff_angle_less_than_min(self):
        self.cud.get_random_open_triangles(0, 3, 3, False)

    @repeat(REPEAT)
    def test__get_random_open_triangles__should_work_for_0_90_angle(self):
        self.cud.get_random_open_triangles(0, 90, 10, False)


class ProcGeoTest500(ATriangleProcGeoTest, unittest.TestCase):

    def get_settings(self):
        return (500, 500), 10, 1


class ProcGeoTest28(ATriangleProcGeoTest, unittest.TestCase):

    def get_settings(self):
        return (28, 28), 2, 0


if __name__ == '__main__':
    unittest.main()
