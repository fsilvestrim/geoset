import numpy as np
import cv2


def get_pts_from_rect(rect):
    box = cv2.boxPoints(rect)
    return np.int0(box)
