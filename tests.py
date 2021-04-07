import numpy as np
from image.image import Image
from utils import opencv
from utils.procgeo import ProcGeo

Image.debug = False

size = 500, 500
line_thickness = 2

if __name__ == "__main__":
    x, y, = None, None
    for i in range(36):
        proc = ProcGeo(size, min_pts_distance=10, margin_safe_area=2)
        image = Image(size)
        bounds = proc.get_random_rect(equal_sides=True, as_points_array=False)
        image.add_simplex(opencv.get_pts_from_rect(bounds), 1)
        image.add_simplex(proc.get_random_rect_rotated(i*10, i*10, as_points_array=True, bounds_rect=bounds), line_thickness)
        image.show()