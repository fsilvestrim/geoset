import warnings

import numpy as np

from utils.opencv import get_pts_from_rect, cv_bl_2_tl


class ProcGeo:
    def __init__(self, bounds, min_pts_distance=10, margin_safe_area=1):
        self.width = bounds[0]
        self.height = bounds[1]
        self.bounds = np.array([*bounds])
        self.safe_bounds = self.bounds - margin_safe_area*2
        self.max_hypot = np.hypot(*bounds)
        self.margin_safe_area = margin_safe_area
        self.min_pts_distance = min_pts_distance

    def __verify_inside_viewport(self, pt, label=None):
        if pt[0] < 0 or pt[1] < 0 or pt[0] > self.width or pt[1] > self.height:
            msg = "point %s(%s) outside of the viewport (%i,%i)" % (
                '' if label is None else label, pt, self.width, self.height)
            raise ValueError(msg)

    @staticmethod
    def safe_randint(low, high):
        low, high = np.int0(low), np.int0(high)
        return low if low == high else np.random.randint(low, high=high)

    @staticmethod
    def get_min_max_bounds(val, minimum, maximum):
        if val > maximum:
            raise ValueError("Value %i is out of bounds of %i" % (val, maximum))

        low = minimum if val >= minimum else -val + minimum
        high = maximum - val if val >= minimum else maximum

        if low >= high:
            raise ValueError(
                "low (%i) is bigger than high (%i). val:%i, min:%i, max:%i" % (low, high, val, minimum, maximum))

        return np.int0(low), np.int0(high)

    @staticmethod
    def get_square_unit_projection(angle, angle_is_in_radians=False):
        angle = angle % np.radians(360) if angle_is_in_radians else np.radians(angle % 360)
        x_projection = 1/np.tan(angle) * (-1 if angle / np.radians(90) > 2 else 1)
        y_projection = np.tan(angle) * (-1 if 1 < angle / np.radians(90) <= 3 else 1)
        return np.round(np.clip(x_projection, -1, 1), 10), np.round(np.clip(y_projection, -1, 1), 10)

    def get_random_line(self, start_angle_range_degree, end_angle_range_degree, as_array=True):
        # get random angle
        angle_degrees = self.safe_randint(start_angle_range_degree, high=end_angle_range_degree)

        # get random length
        scalar_bounds = self.get_square_unit_projection(angle_degrees)
        hypot_max_bounds = np.hypot(*np.multiply(scalar_bounds, self.bounds))
        random_length = np.random.uniform(self.min_pts_distance/hypot_max_bounds)

        # find the new 2d pt from the origin
        pt1 = np.multiply(np.multiply(scalar_bounds, random_length), self.safe_bounds)
        pt1_x_min_max = self.get_min_max_bounds(pt1[0], self.margin_safe_area, self.width - self.margin_safe_area)
        pt1_y_min_max = self.get_min_max_bounds(pt1[1], self.margin_safe_area, self.height - self.margin_safe_area)

        pt0 = np.array([self.safe_randint(pt1_x_min_max[0], high=pt1_x_min_max[1]),
                        self.safe_randint(pt1_y_min_max[0], high=pt1_y_min_max[1])])

        pt0 = np.int0(pt0)
        pt1 = np.int0(pt0 + pt1)

        self.__verify_inside_viewport(pt0, "Line0")
        self.__verify_inside_viewport(pt1, "Line1")

        if as_array:
            return np.array([pt0, pt1])

        return tuple(cv_bl_2_tl(pt0, self.bounds)), tuple(cv_bl_2_tl(pt1, self.bounds ))

    def get_random_open_triangles(self, start_angle_degree, end_angle_degree, min_angle_degree=5, as_array=True):
        if np.diff(end_angle_degree, start_angle_degree) < min_angle_degree:
            raise ValueError("The angle between start (%i) and end (%i) is less than the min angle %i" % (
                start_angle_degree, end_angle_degree, min_angle_degree))

        # get random angle
        p0_angle_degrees = self.safe_randint(start_angle_degree, high=end_angle_degree - min_angle_degree)
        p1_angle_degrees = self.safe_randint(p0_angle_degrees + min_angle_degree, high=end_angle_degree)

        # get max length
        p0_scalar_bounds = self.get_square_unit_projection(p0_angle_degrees)
        p1_scalar_bounds = self.get_square_unit_projection(p1_angle_degrees)
        diff_scalar_bounds = p0_scalar_bounds - p1_scalar_bounds

        random_length = np.random.uniform(self.min_pts_distance_in_square_unit_perc)

        pt0 = np.multiply(np.multiply(p0_scalar_bounds, random_length), self.bounds) - self.margin_safe_area * 2

        # position the 2 random points in the circle unit and scale it
        pt0 = np.array([np.cos(p0_angle_radians) * max_length, np.sin(p0_angle_radians) * max_length])
        pt0_x_min_max = self.get_min_max_bounds(pt0[0], self.margin_safe_area, self.width - self.margin_safe_area)
        pt0_y_min_max = self.get_min_max_bounds(pt0[1], self.margin_safe_area, self.height - self.margin_safe_area)

        pt1 = np.array([np.cos(p1_angle_radians) * max_length, np.sin(p1_angle_radians) * max_length])
        pt1_x_min_max = self.get_min_max_bounds(pt1[0], self.margin_safe_area, self.width - self.margin_safe_area)
        pt1_y_min_max = self.get_min_max_bounds(pt1[1], self.margin_safe_area, self.height - self.margin_safe_area)

        # find the center point
        center_x = np.random.randint(np.maximum(pt0_x_min_max[0], pt1_x_min_max[0]),
                                     high=np.maximum(pt0_x_min_max[1], pt1_x_min_max[1]))
        center_y = np.random.randint(np.maximum(pt0_y_min_max[0], pt1_y_min_max[0]),
                                     high=np.maximum(pt0_y_min_max[1], pt1_y_min_max[1]))
        center = np.array([center_x, center_y])

        # re-position the other points
        pt0 = np.int0(center + pt0)
        pt1 = np.int0(center + pt1)

        self.__verify_inside_viewport(center, "OpenTriC")
        self.__verify_inside_viewport(pt0, "OpenTri0")
        self.__verify_inside_viewport(pt1, "OpenTri1")

        if as_array:
            return np.array([pt0, center, pt1])

        return tuple(pt0), tuple(center), tuple(pt1)

    def get_random_rect(self, as_array=True):
        width = np.random.randint(self.min_pts_distance, high=self.width - self.min_pts_distance)
        height = np.random.randint(self.min_pts_distance, high=self.height - self.min_pts_distance)

        center_x = np.random.randint(self.margin_safe_area + width * .5, high=self.width - width * .5 - self.margin_safe_area)
        center_y = np.random.randint(self.margin_safe_area + height * .5, high=self.height - height * .5 - self.margin_safe_area)

        box = ((center_x, center_y), (width, height), 0)

        pts = get_pts_from_rect(box)

        for idx, pt in enumerate(pts):
            self.__verify_inside_viewport(pt, "Rect%i" % idx)

        if as_array:
            return pts

        return box

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
