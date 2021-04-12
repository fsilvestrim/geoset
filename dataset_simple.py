import concurrent.futures
import os
import time

import numpy as np
from shutil import rmtree
from progress.bar import Bar, ChargingBar, ShadyBar
from augmentation.effects.distorted_image_effect import DistortedImageEffect
from image.image import Image
from procedural.procgeo import ProcGeo

Image.DEBUG = False

categories = 3
samples_per_category = 100
set_size = categories * samples_per_category

image_size = 28, 28
line_thickness = 2
path = "./output/simple"

x = np.empty((set_size, *image_size), dtype=np.float32)
y = np.empty(set_size, dtype=np.uint32)


def new_image(cat_i):
    cat, i = cat_i
    proc = ProcGeo(image_size, 1 if i == 2 else 5, 1)
    image = Image(image_size)

    if cat == 0:
        # vertical line
        image.add_lines(proc.get_random_line(87, 95, False), line_thickness)
    elif cat == 1:
        # diagonal line
        image.add_lines(proc.get_random_line(43, 47, False), line_thickness)
    elif cat == 2:
        # random ellipses
        image.add_ellipse(proc.get_random_rect(True, False), line_thickness)

    if np.random.uniform() >= .5:
        image.set_blur((np.random.randint(1, 5), np.random.randint(1, 5)))

    if np.random.uniform() >= .5:
        image.apply_effect(DistortedImageEffect(0.05))

    image.save("%s/image_%i_%i.png" % (path, cat, i))

    return cat, i, image


if __name__ == "__main__":

    if os.path.exists(path):
        rmtree(path)

    start_time = time.perf_counter()
    bar = Bar('Progress', max=set_size, check_tty=False, suffix='%(percent)d%% [%(index)d / %(max)d]')

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for cat, i, img in executor.map(new_image, np.ndindex((categories, samples_per_category))):
            idx = (cat * samples_per_category) + i
            x[idx] = np.array([img.get_grayscale()])
            y[idx] = cat

            bar.next()

    indexes = np.random.permutation(set_size)
    x, y = x[indexes], y[indexes]

    test_num = np.int0(set_size * .3)
    x_train, y_train = x[:-test_num], y[:-test_num]
    x_test, y_test = x[-test_num:], y[-test_num:]

    np.savez('%s/dataset.npz' % path, x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test)

    bar.finish()

    print("Dataset generated in: %.2f seconds" % (time.perf_counter() - start_time))
