import time
from typing import Tuple, Any

import cv2
import numpy as np
from colour import Color, RGB

from geoset.augmentation.effects.image_effect import ImageEffect


class Image:
    DEBUG = False
    DEFAULT_LINE_THICKNESS = 1
    DEFAULT_LINE_COLOR = RGB.BLACK
    DEFAULT_BACKGROUND_COLOR = RGB.WHITE

    def __init__(self, size: Tuple[int, int], color: Any = DEFAULT_BACKGROUND_COLOR) -> None:
        self.size = size
        self.image = np.zeros((self.size[0], self.size[1], 3), np.uint8)
        self.clear(color)

    @staticmethod
    def get_cvt_color(color: Any):
        if type(color) is not tuple:
            color = Color(color).rgb
        elif type(color) is Color:
            color = color.rgb

        color_hex = [x * 255 for x in color]
        return tuple(reversed(color_hex))
        # return cv2.cvtColor(rgb_color, cv2.COLOR_BGR2RGB)

    def clear(self, color: Any = DEFAULT_BACKGROUND_COLOR) -> None:
        self.image[:] = self.get_cvt_color(color)

    def get_image_copy(self) -> np.array:
        return np.array(self.image, copy=True)

    def set_image(self, image: Any) -> None:
        if type(image) is bytes:
            self.image = np.frombuffer(image, dtype='uint8').reshape((self.size[1], self.size[0], 4))
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            # self.image = np.flip(image, 0).copy(order='C')
        else:
            self.image = image

    def add_ellipse(self, box: Tuple[Tuple[int, int], Tuple[int, int], int],
                    start_angle_degrees: int = 0, end_angle_degrees: int = 360,
                    line_thickness: int = DEFAULT_LINE_THICKNESS,
                    line_color: Any = DEFAULT_LINE_COLOR) -> None:
        cv2.ellipse(self.image, center=box[0], axes=tuple(np.int0(np.multiply(box[1], .5))), angle=box[2],
                    startAngle=start_angle_degrees, endAngle=end_angle_degrees, color=self.get_cvt_color(line_color),
                    thickness=line_thickness)

    def add_simplex(self, bound_pts: np.ndarray, line_thickness: int = DEFAULT_LINE_THICKNESS,
                    line_color: Any = DEFAULT_LINE_COLOR) -> None:
        cv2.drawContours(self.image, [bound_pts], 0, self.get_cvt_color(line_color), line_thickness)

    def add_lines(self, pts: np.ndarray, line_thickness: int = DEFAULT_LINE_THICKNESS,
                  line_color: Any = DEFAULT_LINE_COLOR) -> None:
        prev_pt = None
        line_color_ctv = self.get_cvt_color(line_color)

        for idx, pt in enumerate(pts):
            if Image.DEBUG:
                color_list = list(Color("red").range_to(Color("blue"), len(pts)))
                ctv_color = self.get_cvt_color(color_list[idx].rgb)
                cv2.circle(self.image, pt, 5, ctv_color, 2)

            if not prev_pt is None:
                cv2.line(self.image, prev_pt, pt, line_color_ctv, line_thickness)

            prev_pt = pt

    def set_blur(self, kernel_size: Tuple[int, int]) -> None:
        start_time = time.perf_counter()
        self.image = cv2.GaussianBlur(self.image, kernel_size, 0)

        if Image.DEBUG:
            print("Blur took: %s seconds" % (time.perf_counter() - start_time))

    def apply_effect(self, effect: ImageEffect) -> None:
        start_time = time.perf_counter()

        effect.set_image(self.image)
        self.set_image(effect.render(self.size))
        effect.release()

        if Image.DEBUG:
            print("Effect took: %s seconds" % (time.perf_counter() - start_time))

    def save(self, full_path: str) -> None:
        if full_path.find('.') == -1:
            full_path = full_path + '.png'

        from pathlib import Path
        Path(full_path).parent.mkdir(parents=True, exist_ok=True)

        cv2.imwrite(full_path, self.image)

    def show(self, window_name: str = "Image") -> None:
        if Image.DEBUG:
            print("showing %s" % window_name)

        cv2.imshow(window_name, self.image)
        cv2.waitKey(0)

    def destroy(self) -> None:
        cv2.destroyAllWindows()

    def get_grayscale(self) -> None:
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        gray = cv2.bitwise_not(gray)
        return gray
