import numpy as np

from utils.opencv import get_pts_from_rect


class ProcGeo:
    def __init__(self, bounds, min_pts_distance=10, margin_safe_area=1):
        self.width = bounds[0]
        self.height = bounds[1]
        self.margin_safe_area = margin_safe_area
        self.min_pts_distance = min_pts_distance
        self.max_pts_distance = np.minimum(self.width, self.height) - margin_safe_area

    def get_random_rect(self, as_array=True):
        width = np.random.randint(self.min_pts_distance, high=self.max_pts_distance)
        height = np.random.randint(self.min_pts_distance, high=self.max_pts_distance)

        center_x = np.random.randint(width * .5, high=self.width - width * .5)
        center_y = np.random.randint(height * .5, high=self.height - height * .5)

        box = ((center_x, center_y), (width, height), 0)

        if as_array:
            return get_pts_from_rect(box)

        return box

    def get_random_line(self, as_array=True):
        pt0 = np.random.randint(self.min_pts_distance, high=self.max_pts_distance), np.random.randint(
            self.min_pts_distance, high=self.max_pts_distance)
        pt1 = np.random.randint(self.min_pts_distance, high=self.max_pts_distance), np.random.randint(
            self.min_pts_distance, high=self.max_pts_distance)

        if as_array:
            return np.array([pt0, pt1])

        return pt0, pt1

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
