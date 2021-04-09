import concurrent.futures

import cv2
import time
import noise
import numpy as np

from colour import COLOR_NAME_TO_RGB, Color
from utils import opencv


class Image:
    debug = False

    def __init__(self, size, color="white"):
        self.size = size
        self.width = size[0]
        self.height = size[1]
        self.clear(color)

    def clear(self, color="white"):
        self.image = np.zeros((self.width, self.height, 3), np.uint8)

        ctv_color = opencv.get_cvt_color(Color(color).rgb)
        self.image[:] = ctv_color

    def set_image(self, image):
        if type(image) is bytes:
            self.image = opencv.image_from_bytes(image, self.size)
        else:
            self.image = image

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
        start_time = time.time()
        self.image = cv2.blur(self.image, ksize)
        print("Blur took: %s seconds" % (time.time() - start_time))

    @staticmethod
    def get_noise(image, x, y, scale=100.0, octaves=6, persistence=0.5, lacunarity=2.0):
        pixel = noise.pnoise2(x / scale,
                              y / scale,
                              octaves=octaves,
                              persistence=persistence,
                              lacunarity=lacunarity,
                              repeatx=1024,
                              repeaty=1024,
                              base=0)

        if image is not None:
            image[x][y] = opencv.get_cvt_color([pixel] * 3)

        return 0

    @staticmethod
    def get_perlin_noise(size, scale=100.0, octaves=6, persistence=0.5, lacunarity=2.0):
        start_time = time.perf_counter()

        noise_img = np.zeros((*size, 3), np.uint8)
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for x in range(size[0]):
                for y in range(size[1]):
                    executor.submit(Image.get_noise, noise_img, x, y, scale, octaves, persistence, lacunarity)

        print("Perlin Noise took: %s seconds" % (time.perf_counter() - start_time))

        return noise_img

    def add_displacement_map(self, componentX=0, componentY=0, scaleX=20, scaleY=20, perlin_noise=None):
        displacement_map = perlin_noise if perlin_noise is not None else Image.get_perlin_noise(self.size, 10, 4)

        start_time = time.perf_counter()
        output = np.zeros((self.width, self.height, 3), np.uint8)

        for x in range(output.shape[0]):
            for y in range(output.shape[1]):
                pixel = displacement_map[x, y]
                dx = x + np.int0((pixel[componentX] - 128) * scaleX / 256)
                dy = y + np.int0((pixel[componentY] - 128) * scaleY / 256)

                if dx < 0:
                    dx = 0

                if dx >= output.shape[0]:
                    dx = output.shape[0] - 1

                if dy < 0:
                    dy = 0

                if dy >= output.shape[1]:
                    dy = output.shape[1] - 1

                sampling = self.image[dx, dy]
                output[x, y] = sampling  # opencv.get_cvt_color(Color(color).rgb)

        print("Displacement Map took: %s seconds" % (time.perf_counter() - start_time))

        self.image = output

    def save(self, full_path):
        if full_path.find('.') == -1:
            full_path = full_path + '.png'

        from pathlib import Path
        Path(full_path).parent.mkdir(parents=True, exist_ok=True)

        cv2.imwrite(full_path, self.image)

    def show(self, name="Image"):
        print("showing %s" % name)
        cv2.imshow(name, self.image)
        cv2.waitKey(0)

    def get_grayscale(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        gray = cv2.bitwise_not(gray)
        return gray

    def destroy(self):
        cv2.destroyAllWindows()