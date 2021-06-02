import unittest

from parameterized import parameterized

from geoset.procedural import ProcGeo


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

    @parameterized.expand([
        [0,     1],  # 0
        [45,    1],  # 1
        [90,    2],  # 2
        [135,   2],  # 3
        [180,   3],  # 4
        [225,   3],  # 5
        [270,   4],  # 6
        [315,   4],  # 7
        [360,   1],  # 8
        [360.1, 1],  # 9
    ])
    def test__get_quadrant(self, angle_degrees, expected):
        quadrant = ProcGeo.get_quadrant(angle_degrees)
        self.assertEqual(expected, quadrant, msg="angle:%i" % angle_degrees)

if __name__ == '__main__':
    unittest.main()
