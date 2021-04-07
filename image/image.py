import cv2
import numpy as np

from colour import COLOR_NAME_TO_RGB, Color

from utils import opencv


class Image:
    debug = False

    def __init__(self, bounds, color="white"):
        self.width = bounds[0]
        self.height = bounds[1]
        self.image = self.__create_viewport(color)

    def __create_viewport(self, color):
        ctv_color = opencv.get_cvt_color(Color(color).rgb)
        image = np.zeros((self.width, self.height, 3), np.uint8)
        image[:] = ctv_color

        return image

    def add_ellipse(self, bounds, line_thickness=1, line_color="black"):
        line_color_ctv = opencv.get_cvt_color(Color(line_color).rgb)
        cv2.ellipse(self.image, bounds, line_color_ctv, line_thickness)

    def add_simplex(self, bound_pts, line_thickness=1, line_color="black"):
        line_color_ctv = opencv.get_cvt_color(Color(line_color).rgb)
        cv2.drawContours(self.image, [bound_pts], 0, line_color_ctv, line_thickness)

    def add_lines(self, pts, line_thickness=1, line_color="black"):
        prev_pt = None
        line_color_ctv = opencv.get_cvt_color(Color(line_color).rgb)
        for idx, pt in enumerate(pts):
            if Image.debug:
                color_list = list(Color("red").range_to(Color("blue"), len(pts)))
                ctv_color = opencv.get_cvt_color(color_list[idx].rgb)
                cv2.circle(self.image, pt, 5, ctv_color, 2)
            if not prev_pt is None:
                cv2.line(self.image, prev_pt, pt, line_color_ctv, line_thickness)
            prev_pt = pt

    def set_blur(self, ksize):
        self.image = cv2.blur(self.image, ksize)

    def save(self, full_path):
        if full_path.find('.') == -1:
            full_path = full_path + '.png'

        from pathlib import Path
        Path(full_path).parent.mkdir(parents=True, exist_ok=True)

        cv2.imwrite(full_path, self.image)

    def show(self, name="Image"):
        cv2.imshow(name, self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def get_grayscale(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        gray = cv2.bitwise_not(gray)
        return gray
