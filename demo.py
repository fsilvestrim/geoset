import numpy as np
from image.image import Image
from utils.procgeo import ProcGeo

Image.debug = False

size = 28, 28
line_thickness = 2

#todo: max-size lines, triangle, rotated elipses, glitch rectangle blue

if __name__ == "__main__":
    for i in range(500):
        proc = ProcGeo(size, 1, 0)
        image = Image(size)

        # vertical line
        # id = 0
        # image.add_lines(proc.get_random_line(87, 95, False), line_thickness)

        # diagonal line
        # id = 1
        # image.add_lines(proc.get_random_line(43, 47, False), line_thickness)

        # random ellipses
        id = 2
        image.add_ellipse(proc.get_random_rect(False), line_thickness)

        if np.random.uniform() >= .5:
            image.set_blur((np.random.randint(1, 5), np.random.randint(1, 5)))

        image.save("./output/image_%i_%i.png" % (id, i))
