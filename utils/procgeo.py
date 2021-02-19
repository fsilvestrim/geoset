import warnings

import numpy as np

from utils.opencv import get_pts_from_rect


class ProcGeo:
    def __init__(self, bounds, min_pts_distance=10, margin_safe_area=1):
        self.width = bounds[0]
        self.height = bounds[1]
        self.margin_safe_area = margin_safe_area
        self.min_pts_distance = min_pts_distance
        self.max_pts_distance = np.minimum(self.width, self.height) - margin_safe_area

    def __verify_inside_viewport(self, pt, label=None):
        if pt[0] < 0 or pt[1] < 0 or pt[0] > self.width or pt[1] > self.height:
            warnings.warn("point %s(%s) outside of the viewport (%i,%i)" % (
            '' if label is None else label, pt, self.width, self.height), Warning)

    def get_random_rect(self, as_array=True):
        width = np.random.randint(self.min_pts_distance, high=self.max_pts_distance)
        height = np.random.randint(self.min_pts_distance, high=self.max_pts_distance)

        center_x = np.random.randint(width * .5, high=self.width - width * .5)
        center_y = np.random.randint(height * .5, high=self.height - height * .5)

        box = ((center_x, center_y), (width, height), 0)

        pts = get_pts_from_rect(box)

        for idx, pt in enumerate(pts):
            self.__verify_inside_viewport(pt, "Rect%i" % idx)

        if as_array:
            return pts

        return box

    def get_random_line(self, as_array=True):
        pt0 = np.random.randint(self.min_pts_distance, high=self.max_pts_distance), np.random.randint(
            self.min_pts_distance, high=self.max_pts_distance)
        pt1 = np.random.randint(self.min_pts_distance, high=self.max_pts_distance), np.random.randint(
            self.min_pts_distance, high=self.max_pts_distance)

        self.__verify_inside_viewport(pt0, "Line0")
        self.__verify_inside_viewport(pt1, "Line1")

        if as_array:
            return np.array([pt0, pt1])

        return pt0, pt1

    def __get_min_bounds(self, val, minimum):
        return -val if val < minimum else minimum

    def __get_max_bounds(self, val, maximum):
        return maximum - val if val > maximum else maximum

    def __get_min_max_bounds(self, val0, val1, min_size, max_size):
        bounds_min = np.maximum(self.__get_min_bounds(val0, min_size), \
                                self.__get_min_bounds(val1, min_size))

        bounds_max = np.maximum(self.__get_max_bounds(val0, max_size), \
                                self.__get_max_bounds(val1, max_size))

        return bounds_min, bounds_max

    def get_random_open_triangles(self, start_angle_degree, end_angle_degree, min_angle_degree=5, as_array=True):
        start_angle = np.radians(np.random.randint(start_angle_degree, high=end_angle_degree))
        end_angle = np.radians(np.random.randint(start_angle_degree + min_angle_degree, high=end_angle_degree))

        length = np.random.randint(self.min_pts_distance, high=self.max_pts_distance)

        pt0 = np.array([np.cos(start_angle) * length, np.sin(start_angle) * length])
        pt1 = np.array([np.cos(end_angle) * length, np.sin(end_angle) * length])

        center_x_min_max = self.__get_min_max_bounds(pt0[0], pt1[0], self.min_pts_distance,
                                                     self.width - self.margin_safe_area)

        center_y_min_max = self.__get_min_max_bounds(pt0[1], pt1[1], self.min_pts_distance,
                                                     self.height - self.margin_safe_area)

        center = np.array([np.random.randint(center_x_min_max[0], high=center_x_min_max[1]), \
                           np.random.randint(center_y_min_max[0], high=center_y_min_max[1])])

        pt0 = np.int0(center + pt0)
        pt1 = np.int0(center + pt1)

        self.__verify_inside_viewport(center, "OpenTriC")
        self.__verify_inside_viewport(pt0, "OpenTri0")
        self.__verify_inside_viewport(pt1, "OpenTri1")

        if as_array:
            return np.array([pt0, center, pt1])

        return tuple(pt0), tuple(center), tuple(pt1)

    def get_random_box2(self):
        # - select a direction on a unit circle
        # - calculate the distance to the nearest edge
        # - select another point in that direction with dist < the distance to the edge
        # - select another direction
        # - check distances from point A and point B to the nearest edges
        # - pick the smallest between the 2, walk dist < dist to smallest edge

        # angle = np.random.randint(0, high=180)
        # theta = np.radians(angle)

        # - select a random point
        pt0 = np.random.randint(self.min_pts_distance, high=self.max_pts_distance), np.random.randint(
            self.min_pts_distance, high=self.max_pts_distance)

        # VT = np.array([[0, 0], [0, width - line_thickness]])
        # VA = np.array([[A[0], A[1]], [np.cos(theta) + 1, np.sin(theta) + 1]])
        # DT = np.vdot(VT, VA)
        #
        # DC = np.random.randint(min_size, high=DT)
        # B = [A[0] + np.cos(theta) * DC, A[1] + np.sin(theta) * DC]
        # C = [D[0] + np.cos(theta) * DC, D[1] + np.sin(theta) * DC]
        return np.array([])
