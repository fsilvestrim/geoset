import cv2

from augmentation.effects.distorted_image_effect import DistortedImageEffect
from image.image import Image
from utils import opencv
from utils.procgeo import ProcGeo

Image.DEBUG = False

size = 500, 500
line_thickness = 2

if __name__ == "__main__":
    x, y, = None, None
    perlin_noise_image = cv2.imread('perlin_noise.png', cv2.IMREAD_COLOR)

    for i in range(1):
        proc = ProcGeo(size, min_pts_distance=10, margin_safe_area=2)
        image = Image(size)
        bounds = proc.get_random_rect(equal_sides=True, as_points_array=False)
        image.add_simplex(opencv.get_pts_from_rect(bounds), 1)
        # image.add_ellipse(proc.get_random_rect_rotated(i*10, i*10, as_points_array=False, bounds_rect=bounds), line_thickness)
        # Image.get_perlin_noise(image.bounds, 10, 4)
        # image.add_displacement_map()
        # original_image = np.array(image.image, copy=True)
        # image.show()
        # image.clear()
        # image.show()
        # start_time = time.perf_counter()
        # distorced_image = opengl.get_new_image(size, original_image, perlin_noise_image)
        # print("Dispacement took: %s seconds" % (time.perf_counter() - start_time))
        # image.apply_effect(Effect())
        # image.apply_effect(DefaultImageEffect())
        image.apply_effect(DistortedImageEffect(perlin_noise_image))
        image.show()
