import numpy as np
import cv2


def get_cvt_color(scalar_color):
    color_hex = [x * 255 for x in scalar_color]
    return tuple(reversed(color_hex))
    # return cv2.cvtColor(rgb_color, cv2.COLOR_BGR2RGB)


def get_pts_from_rect(rect):
    box = cv2.boxPoints(rect)
    return np.int0(box)


def cv_bl_2_tl(pt, bounds):
    return pt[0], bounds[1] - pt[1]
