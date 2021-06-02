import os
import random
from typing import Tuple

import numpy as np

from enum import Enum

from geoset.augmentation.effects.distorted_image_effect import DistortedImageEffect
from geoset.dataset.dataset import Dataset
from geoset.image.image import Image
from geoset.procedural.procgeo import ProcGeo


class SimpleDataset2(Dataset):
    class Category(Enum):
        VERTICAL_LINE = 0
        HORIZONTAL_LINE = 1
        DIAGONAL_LINE = 2
        ELLIPSE = 3
        GREATER_THAN = 4
        LOWER_THAN = 5

    def __init__(self, samples_per_category: int, image_size: Tuple[int, int],
                 destination: str, stroke_thickness: int = 2, save_images: bool = False) -> None:
        self.__save_images = save_images
        self.__stroke_thickness = stroke_thickness

        super().__init__(len(self.Category), samples_per_category, image_size, destination)

    def _generate_image(self, ci_si: Tuple[int, int]) -> Tuple[int, int, np.array]:
        category_idx, sample_idx = ci_si

        image = Image(self._image_size)

        proc = ProcGeo(self._image_size,
                       min_pts_distance=8 if category_idx == self.Category.ELLIPSE.value else 10,
                       margin_safe_area=1)

        if self.Category.VERTICAL_LINE.value == category_idx:
            image.add_lines(proc.get_random_line(90, 15, False), self.__stroke_thickness)
        elif self.Category.HORIZONTAL_LINE.value == category_idx:
            image.add_lines(proc.get_random_line(180, 15, False), self.__stroke_thickness)
        elif self.Category.DIAGONAL_LINE.value == category_idx:
            image.add_lines(proc.get_random_line(45, 15, False), self.__stroke_thickness)
        elif self.Category.ELLIPSE.value == category_idx:
            image.add_ellipse(proc.get_random_rect(True, False), 0, 360, self.__stroke_thickness)
        elif self.Category.GREATER_THAN.value == category_idx:
            image.add_lines(proc.get_random_open_triangles(135, 225, 10, False), self.__stroke_thickness)
        elif self.Category.LOWER_THAN.value == category_idx:
            image.add_lines(proc.get_random_open_triangles(45, 315, 10, False), self.__stroke_thickness)

        if np.random.uniform() >= .5:
            image.set_blur((random.randrange(1, 10, 2), random.randrange(1, 10, 2)))

        if np.random.uniform() >= .5:
            image.apply_effect(DistortedImageEffect(np.random.uniform(0.01, 0.1)))

        if self.__save_images:
            path = f'{self._destination}/{self.name}'
            os.makedirs(path)
            image.save(f'{path}/image_{category_idx}_{sample_idx}.png')

        return category_idx, sample_idx, np.array([image.get_grayscale()])
