import warnings

import numpy as np

from utils.opencv import get_pts_from_rect


class ProcGeo:
    def __init__(self, bounds, min_pts_distance=10, margin_safe_area=1):
        self.width = bounds[0]
        self.height = bounds[1]
        self.margin_safe_area = margin_safe_area
        self.min_pts_distance = min_pts_distance

    def __verify_inside_viewport(self, pt, label=None):
        if pt[0] < 0 or pt[1] < 0 or pt[0] > self.width or pt[1] > self.height:
            msg = "point %s(%s) outside of the viewport (%i,%i)" % (
                '' if label is None else label, pt, self.width, self.height)
            raise ValueError(msg)

    @staticmethod
    def get_min_max_bounds(val, minimum, maximum):
        if val > maximum:
            raise ValueError("Value %i is out of bounds of %i" % (val, maximum))

        low = minimum if val >= minimum else -val + minimum
        high = maximum - val if val >= minimum else maximum

        if low >= high:
            raise ValueError(
                "low (%i) is bigger than high (%i). val:%i, min:%i, max:%i" % (low, high, val, minimum, maximum))

        return low, high

    @staticmethod
    def get_square_unit_projection(angle, angle_is_in_radians=False):
        angle = angle % np.radians(360) if angle_is_in_radians else np.radians(angle % 360)
        x_projection = 1/np.tan(angle) * (-1 if angle / np.radians(90) > 2 else 1)
        y_projection = np.tan(angle) * (-1 if 1 < angle / np.radians(90) <= 3 else 1)
        return np.round(np.clip(x_projection, -1, 1), 10), np.round(np.clip(y_projection, -1, 1), 10)

    def get_max_projection(self, angle, convert_to_radians=False):
        x, y = self.get_square_unit_projection(angle, convert_to_radians)

        # now we know the longest length
        max_length_x = np.clip(np.abs(x), 0, 1) * (self.width - self.margin_safe_area * 2)
        max_length_y = np.clip(np.abs(y), 0, 1) * (self.height - self.margin_safe_area * 2)

        return np.hypot(max_length_x, max_length_y)

    def get_random_line(self, start_angle_range_degree, end_angle_range_degree, as_array=True):
        # get random angle
        angle_radians = np.radians(np.random.randint(start_angle_range_degree, high=end_angle_range_degree)
                                   if start_angle_range_degree != end_angle_range_degree else start_angle_range_degree)

        # get random length
        length = np.random.randint(self.min_pts_distance, high=self.get_max_projection(angle_radians))

        # find the new 2d pt from the origin
        pt1 = np.array([np.cos(angle_radians) * length, np.sin(angle_radians) * length])
        pt1_x_min_max = self.get_min_max_bounds(pt1[0], self.margin_safe_area, self.width - self.margin_safe_area)
        pt1_y_min_max = self.get_min_max_bounds(pt1[1], self.margin_safe_area, self.height - self.margin_safe_area)

        pt0 = np.array([
            np.random.randint(pt1_x_min_max[0], high=pt1_x_min_max[1])
            if pt1_x_min_max[0] != pt1_x_min_max[1] else pt1_x_min_max[0],
            np.random.randint(pt1_y_min_max[0], high=pt1_y_min_max[1])
            if pt1_y_min_max[0] != pt1_y_min_max[1] else pt1_y_min_max[0]])

        pt0 = np.int0(pt0)
        pt1 = np.int0(pt0 + pt1)

        self.__verify_inside_viewport(pt0, "Line0")
        self.__verify_inside_viewport(pt1, "Line1")

        if as_array:
            return np.array([pt0, pt1])

        return tuple(pt0), tuple(pt1)

    def get_random_open_triangles(self, start_angle_degree, end_angle_degree, min_angle_degree=5, as_array=True):
        if np.diff(end_angle_degree, start_angle_degree) < min_angle_degree:
            raise ValueError("The angle between start (%i) and end (%i) is less than the min angle %i" % (
                start_angle_degree, end_angle_degree, min_angle_degree))

        # get random angle
        p0_angle_radians = np.radians(np.random.randint(start_angle_degree, high=end_angle_degree))
        p1_angle_radians = np.radians(np.random.randint(start_angle_degree + min_angle_degree, high=end_angle_degree))

        # get max length
        p0_max_lengths = self.get_max_projection(p0_angle_radians)
        p1_max_lengths = self.get_max_projection(p1_angle_radians)

        # max_ = (self.min_pts_distance, high=self.get_max_length(start_radians))
        end_length = np.random.randint(self.min_pts_distance, high=self.get_max_projection(p1_angle_radians))
        max_length = 0
        length = np.random.randint(self.min_pts_distance, high=max_length)

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
