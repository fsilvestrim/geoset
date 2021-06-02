from collections import Iterable

import cv2
import numpy as np


class ProcGeo:
    def __init__(self, bounds, min_pts_distance=10, margin_safe_area=1):
        self.width = bounds[0]
        self.height = bounds[1]
        self.bounds = np.array([*bounds])
        self.safe_bounds = self.bounds - margin_safe_area * 2
        self.max_hypot = np.hypot(*bounds)
        self.margin_safe_area = margin_safe_area
        self.min_pts_distance = min_pts_distance

    def __verify_inside_viewport(self, pt, label=None):
        if pt[0] < 0 or pt[1] < 0 or pt[0] > self.width or pt[1] > self.height:
            msg = "point %s(%s) outside of the viewport (%i,%i)" % (
                '' if label is None else label, pt, self.width, self.height)
            raise ValueError(msg)

    @staticmethod
    def get_pts_from_rect(rect):
        box = cv2.boxPoints(rect)
        return np.int0(box)

    @staticmethod
    def cv_bl_2_tl(pts, bounds):
        fn_projection = lambda pt: (pt[0], bounds[1] - pt[1])

        if isinstance(pts, Iterable):
            converted_points = []
            for pt in pts:
                converted_points.append(fn_projection(pt))
            return tuple(converted_points)

        return tuple(fn_projection(pts))

    @staticmethod
    def safe_randint(low, high):
        low, high = np.int0(low), np.int0(high)

        if low > high:
            raise ValueError("Value low %i is bigger than high %i" % (low, high))

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
    def get_capped_angle_in_radians(angle, max_angle=360, angle_is_in_radians=False):
        return angle % np.radians(max_angle) if angle_is_in_radians else np.radians(angle % max_angle)

    @staticmethod
    def get_safe_angle(angle_in_degrees):
        return angle_in_degrees if angle_in_degrees > 0 else 360 - angle_in_degrees

    @staticmethod
    def get_quadrant(angle, angle_is_in_radians=False):
        angle = angle if angle_is_in_radians else np.radians(angle)
        quadrant = 1 + np.int0((angle / np.radians(90)) % 4)
        return quadrant

    @staticmethod
    def get_square_unit_projection(angle, angle_is_in_radians=False):
        angle_radians = ProcGeo.get_capped_angle_in_radians(angle, angle_is_in_radians=angle_is_in_radians)
        quadrant = ProcGeo.get_quadrant(angle_radians, angle_is_in_radians=True)

        tan = np.tan(angle_radians)
        cot = 1 if tan == 0 else 1 / tan

        x_projection = np.round(np.clip(np.abs(cot) * (-1 if 1 < quadrant <= 3 else 1), -1, 1), 10)
        y_projection = np.round(np.clip(np.abs(tan) * (-1 if 2 < quadrant <= 4 else 1), -1, 1), 10)

        # print("angle %i, quadrant % i => %.2f, %.2f" % (angle, quadrant, x_projection, y_projection))

        return x_projection, y_projection

    @staticmethod
    def get_circle_unit_projection(angle, angle_is_in_radians=False):
        angle_radians = ProcGeo.get_capped_angle_in_radians(angle, angle_is_in_radians=angle_is_in_radians)

        x_projection = np.round(np.cos(angle_radians), 10)
        y_projection = np.round(np.sin(angle_radians), 10)

        # print("angle %i => %.2f, %.2f" % (angle, x_projection, y_projection))

        return x_projection, y_projection

    @staticmethod
    def get_box_size(points):
        box = [0, 0]

        for point in points:
            box[0] = np.maximum(box[0], np.abs(point[0]))
            box[1] = np.minimum(box[1], np.abs(point[1]))

        return box

    @staticmethod
    def _get_values(values, as_array):
        if as_array:
            return np.array([*values])

        return values

    def get_random_line(self, target_angle_in_degree, degree_of_freedom, as_points_array=True):
        # get random angle
        half_degree_of_freedom = degree_of_freedom * .5
        angle_degrees = self.safe_randint(target_angle_in_degree - half_degree_of_freedom,
                                          high=target_angle_in_degree + half_degree_of_freedom)

        # get random length
        scalar_bounds = self.get_square_unit_projection(angle_degrees)
        hypot_max_bounds = np.hypot(*np.multiply(scalar_bounds, self.bounds))
        random_length = np.random.uniform(self.min_pts_distance / hypot_max_bounds)

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

        points = ProcGeo.cv_bl_2_tl([pt0, pt1], self.bounds)
        return ProcGeo._get_values(points, as_points_array)

    def get_random_open_triangles(self, start_angle_degree, end_angle_degree, degree_of_freedom, as_points_array=True):
        # if np.diff(end_angle_degree, start_angle_degree) < degree_of_freedom * 2:
        #     raise ValueError("The angle between start (%i) and end (%i) is less than the degree of freedom %i" % (
        #         start_angle_degree, end_angle_degree, degree_of_freedom))

        # get random angle
        half_degree_of_freedom = self.safe_randint(0, degree_of_freedom * .5)

        # find direction of the angles
        if np.abs(start_angle_degree - end_angle_degree) < 180:
            # inner (+start -end)
            p0_angle_degrees = self.get_safe_angle(start_angle_degree + half_degree_of_freedom)
            p1_angle_degrees = self.get_safe_angle(end_angle_degree - half_degree_of_freedom)
        else:
            # outer (-start + end)
            p0_angle_degrees = self.get_safe_angle(start_angle_degree - half_degree_of_freedom)
            p1_angle_degrees = self.get_safe_angle(end_angle_degree + half_degree_of_freedom)

        # get random bounding box
        random_bounding_box = self.get_random_rect(equal_sides=True, as_points_array=False)
        center = np.array(random_bounding_box[0])
        size = np.array(random_bounding_box[1])

        # project the two points inside the random bounding box
        projected_pt0 = ProcGeo.get_circle_unit_projection(p0_angle_degrees)
        projected_pt1 = ProcGeo.get_circle_unit_projection(p1_angle_degrees)

        # remap the points
        pt0 = np.int0(center + projected_pt0 * size * .5)
        pt1 = np.int0(center + projected_pt1 * size * .5)

        self.__verify_inside_viewport(center, "OpenTriC")
        self.__verify_inside_viewport(pt0, "OpenTri0")
        self.__verify_inside_viewport(pt1, "OpenTri1")

        points = ProcGeo.cv_bl_2_tl([pt0, center, pt1], self.bounds)
        return ProcGeo._get_values(points, as_points_array)

    def get_random_rect(self, equal_sides=False, as_points_array=True):
        if not equal_sides:
            width = self.safe_randint(self.min_pts_distance, high=self.safe_bounds[0] - self.min_pts_distance)
            height = self.safe_randint(self.min_pts_distance, high=self.safe_bounds[1] - self.min_pts_distance)
        else:
            width = height = self.safe_randint(self.min_pts_distance,
                                               high=np.minimum(*self.safe_bounds) - self.min_pts_distance)

        center_x = self.safe_randint(self.margin_safe_area + width * .5,
                                     high=self.width - width * .5 - self.margin_safe_area)
        center_y = self.safe_randint(self.margin_safe_area + height * .5,
                                     high=self.height - height * .5 - self.margin_safe_area)

        box = ((center_x, center_y), (width, height), 0)
        pts = self.get_pts_from_rect(box)

        for idx, pt in enumerate(pts):
            self.__verify_inside_viewport(pt, "Rect%i" % idx)

        if as_points_array:
            return pts

        return box

    def get_random_rect_rotated(self, start_angle_range_degree=0, end_angle_range_degree=359,
                                as_points_array=True, bounds_rect=None):
        # get random bounding box
        random_bounding_box = self.get_random_rect(equal_sides=True,
                                                   as_points_array=False) if bounds_rect is None else bounds_rect
        center = np.array(random_bounding_box[0])
        size = np.array(random_bounding_box[1])

        # get random
        # angle
        angle_degrees = self.safe_randint(start_angle_range_degree, high=end_angle_range_degree)

        # find length
        scalar_bounds = self.get_square_unit_projection(angle_degrees)
        hypot_max_bounds = np.hypot(*np.multiply(scalar_bounds, size))
        width = self.safe_randint(np.maximum(size[1] * .5, self.min_pts_distance),
                                  high=hypot_max_bounds - self.min_pts_distance)

        # find height
        rest_width = hypot_max_bounds - width
        height = self.safe_randint(self.min_pts_distance, high=rest_width)

        box = (center, (width, height), 180 - angle_degrees)
        pts = self.get_pts_from_rect(box)

        for idx, pt in enumerate(pts):
            self.__verify_inside_viewport(pt, "Rect%i" % idx)

        if as_points_array:
            return pts

        return box
