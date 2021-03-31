import numpy as np
from image.image import Image
from utils.procgeo import ProcGeo

Image.debug = False

size = 500, 500
line_thickness = 2

if __name__ == "__main__":
    x, y, = None, None
    for i in range(10):
        proc = ProcGeo(size, 0)
        image = Image(size)
        image.add_lines(proc.get_random_open_triangles(80, 45, 0, False), line_thickness)
        image.show()