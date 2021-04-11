from typing import Tuple, Any

import cv2
import numpy as np

from collections import Iterable

from colour import Color


def image_to_byte_array(image):
    image = np.frombuffer(image, dtype='uint8').reshape((image.shape[1], image.shape[0], 3)).tobytes()
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image


def image_from_bytes(image_bytes, size):
    image = np.frombuffer(image_bytes, dtype='uint8').reshape((size[1], size[0], 4))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # image = np.flip(image, 0).copy(order='C')
    return image


def get_cvt_color(color: Any):
    if type(color) is not tuple:
        color = Color(color).rgb
    elif type(color) is Color:
        color = color.rgb

    color_hex = [x * 255 for x in color]
    return tuple(reversed(color_hex))
    # return cv2.cvtColor(rgb_color, cv2.COLOR_BGR2RGB)


def get_pts_from_rect(rect):
    box = cv2.boxPoints(rect)
    return np.int0(box)


def get_grayscale(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    return gray


def cv_bl_2_tl(pts, bounds):
    fn_projection = lambda pt: (pt[0], bounds[1] - pt[1])

    if isinstance(pts, Iterable):
        converted_points = []
        for pt in pts:
            converted_points.append(fn_projection(pt))
        return tuple(converted_points)

    return tuple(fn_projection(pts))
