from image.image import Image
from utils.procgeo import ProcGeo

Image.debug = True

size = 500, 500
if __name__ == "__main__":
    for i in range(361):
        proc = ProcGeo(size)
        print("%i => %s" % (i, proc.get_square_unit_projection(i)))
        # image = Image(size)
        # image.add_lines(proc.get_random_line(43, 47, False))
        # image.add_lines(proc.get_random_line(44, 44, False))
        # image.add_lines(proc.get_random_line(87, 95, False))
        # image.add_simplex(proc.get_random_rect())
        # image.add_lines(proc.get_random_open_triangles(0, 360, 5, False))
        # image.add_ellipse(proc.get_random_rect(False))
        # image.show()
