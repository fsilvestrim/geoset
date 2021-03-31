import numpy as np
from image.image import Image
from utils.procgeo import ProcGeo

Image.debug = False

size = 28, 28
line_thickness = 2

# todo: max-size lines, triangle, rotated elipses, glitch rectangle blue

if __name__ == "__main__":
    x, y, = None, None
    for cat in range(3):
        for i in range(100):
            proc = ProcGeo(size, 1 if i == 2 else 5, 1)
            image = Image(size)

            if cat == 0:
                # vertical line
                image.add_lines(proc.get_random_line(87, 95, False), line_thickness)
            elif cat == 1:
                # diagonal line
                image.add_lines(proc.get_random_line(43, 47, False), line_thickness)
            elif cat == 2:
                # random ellipses
                image.add_ellipse(proc.get_random_rect(False), line_thickness)

            if np.random.uniform() >= .5:
                image.set_blur((np.random.randint(1, 5), np.random.randint(1, 5)))

            if x is None:
                x = np.array([image.get_grayscale()])
                y = np.array([cat])
            else:
                x = np.concatenate((x, np.array([image.get_grayscale()])), axis=0)
                y = np.append(y, cat)

            image.save("./output/image_%i_%i.png" % (cat, i))

    amount = len(x)
    indexes = np.random.permutation(amount)
    x, y = x[indexes], y[indexes]

    test_num = np.int0(amount * .3)
    x_train, y_train = x[:-test_num], y[:-test_num]
    x_test, y_test = x[-test_num:], y[-test_num:]

    np.savez('./output/geocam.npz', x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test)
