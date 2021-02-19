import numpy as np
import cv2

from utils import color


class Image:
    def __init__(self, bounds, rgb_color=color.white):
        self.width = bounds[0]
        self.height = bounds[1]
        self.color = color.get_cv_color(rgb_color)
        self.image = self.__create_viewport()

    def __create_viewport(self):
        image = np.zeros((self.width, self.height, 3), np.uint8)
        image[:] = self.color

        return image

    def add_ellipse(self, bound_pts, line_thickness=1, line_color=color.black):
        cv2.ellipse(self.image, bound_pts, line_color, line_thickness)

    def add_simplex(self, bound_pts, line_thickness=1, line_color=color.black):
        cv2.drawContours(self.image, [bound_pts], 0, line_color, line_thickness)

    def add_lines(self, pts, line_thickness=1, line_color=color.black):
        prev_pt = None
        for pt in pts:
            if not prev_pt is None:
                cv2.line(self.image, prev_pt, pt, line_color, line_thickness)
            prev_pt = pt

    def set_blur(self, ksize):
        return cv2.blur(self.image, ksize)

    def save(self, full_path):
        if full_path.find('.') == -1:
            full_path = full_path + '.png'

        cv2.imwrite(full_path, self.image)

    def show(self, name="Image"):
        cv2.imshow(name, self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
