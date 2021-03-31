from collections import Iterable

import numpy as np
import cv2


def get_cvt_color(scalar_color):
    color_hex = [x * 255 for x in scalar_color]
    return tuple(reversed(color_hex))
    # return cv2.cvtColor(rgb_color, cv2.COLOR_BGR2RGB)


def get_pts_from_rect(rect):
    box = cv2.boxPoints(rect)
    return np.int0(box)


def cv_bl_2_tl(pts, bounds):
    fn_projection = lambda pt: (pt[0], bounds[1] - pt[1])

    if isinstance(pts, Iterable):
        converted_points = []
        for pt in pts:
            converted_points.append(fn_projection(pt))
        return tuple(converted_points)

    return tuple(fn_projection(pts))
