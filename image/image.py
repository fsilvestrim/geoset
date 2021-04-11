import time
from typing import Tuple, Any

import cv2
import numpy as np
from colour import Color, RGB

from augmentation.effects.image_effect import ImageEffect
from utils import opencv


class Image:
    DEBUG = False
    DEFAULT_LINE_THICKNESS = 1
    DEFAULT_LINE_COLOR = RGB.BLACK
    DEFAULT_BACKGROUND_COLOR = RGB.WHITE

    def __init__(self, size: Tuple[int, int], color: Any = DEFAULT_BACKGROUND_COLOR):
        self.size = size
        self.image = np.zeros((self.size[0], self.size[1], 3), np.uint8)
        self.clear(color)

    def clear(self, color: Any = DEFAULT_BACKGROUND_COLOR) -> None:
        self.image[:] = opencv.get_cvt_color(color)

    def get_image_copy(self) -> np.array:
        return np.array(self.image, copy=True)

    def set_image(self, image: Any) -> None:
        if type(image) is bytes:
            self.image = opencv.image_from_bytes(image, self.size)
        else:
            self.image = image

    def add_ellipse(self, bounds: Tuple[Tuple[int, int], Tuple[int, int], int],
                    line_thickness: int = DEFAULT_LINE_THICKNESS, line_color: Any = DEFAULT_LINE_COLOR) -> None:
        cv2.ellipse(self.image, bounds, opencv.get_cvt_color(line_color), line_thickness)

    def add_simplex(self, bound_pts: np.ndarray, line_thickness: int = DEFAULT_LINE_THICKNESS,
                    line_color: Any = DEFAULT_LINE_COLOR) -> None:
        cv2.drawContours(self.image, [bound_pts], 0, opencv.get_cvt_color(line_color), line_thickness)

    def add_lines(self, pts: np.ndarray, line_thickness: int = DEFAULT_LINE_THICKNESS,
                  line_color: Any = DEFAULT_LINE_COLOR) -> None:
        prev_pt = None
        line_color_ctv = opencv.get_cvt_color(line_color)

        for idx, pt in enumerate(pts):
            if Image.DEBUG:
                color_list = list(Color("red").range_to(Color("blue"), len(pts)))
                ctv_color = opencv.get_cvt_color(color_list[idx].rgb)
                cv2.circle(self.image, pt, 5, ctv_color, 2)

            if not prev_pt is None:
                cv2.line(self.image, prev_pt, pt, line_color_ctv, line_thickness)

            prev_pt = pt

    def set_blur(self, kernel_size: float) -> None:
        start_time = time.time()
        self.image = cv2.blur(self.image, kernel_size)
        print("Blur took: %s seconds" % (time.time() - start_time))

    def apply_effect(self, effect: ImageEffect) -> None:
        effect.set_image(self.image)
        self.set_image(effect.render(self.size))

    def save(self, full_path: str) -> None:
        if full_path.find('.') == -1:
            full_path = full_path + '.png'

        from pathlib import Path
        Path(full_path).parent.mkdir(parents=True, exist_ok=True)

        cv2.imwrite(full_path, self.image)

    def show(self, window_name: str = "Image") -> None:
        print("showing %s" % window_name)
        cv2.imshow(window_name, self.image)
        cv2.waitKey(0)

    def destroy(self) -> None:
        cv2.destroyAllWindows()
