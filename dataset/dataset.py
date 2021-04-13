import abc
import concurrent.futures
import os
import time
from shutil import rmtree
from typing import Tuple

import cv2
from PIL import Image, ImageOps

import numpy as np
from progress.bar import Bar


class Dataset(metaclass=abc.ABCMeta):
    def __init__(self, categories_amount: int, samples_per_category: int, image_size: Tuple[int, int],
                 destination: str) -> None:
        self._image_size = image_size
        self._destination = destination

        self.__num_categories = categories_amount
        self.__num_samples = samples_per_category

        self.__total_samples = categories_amount * samples_per_category
        self.__x = np.empty((self.__total_samples, *image_size), dtype=np.float32)
        self.__y = np.empty(self.__total_samples, dtype=np.uint32)

        self.clear()

    def _get_image_idx(self, category, sample):
        return (category * self.__num_samples) + sample

    def clear(self):
        if os.path.exists(self._destination):
            rmtree(self._destination)

        os.makedirs(self._destination)

    def generate(self):
        start_time = time.perf_counter()
        bar = Bar('Progress', max=self.__total_samples, check_tty=False, suffix='%(percent)d%% [%(index)d / %(max)d]')

        with concurrent.futures.ProcessPoolExecutor() as executor:
            for category_idx, sample_idx, image in \
                    executor.map(self._generate_image, np.ndindex((self.__num_categories, self.__num_samples))):
                dataset_idx = self._get_image_idx(category_idx, sample_idx)
                self.__x[dataset_idx] = image
                self.__y[dataset_idx] = category_idx
                bar.next()

        bar.finish()

        print("Dataset Created! "
              "\n\tName: %s "
              "\n\tCategories:%d "
              "\n\tSamples:%d "
              "\n\tTotal:%d "
              "\n\tDestination:%s "
              "\n\tTook:%.2fs" %
              (self.__class__.__name__, self.__num_categories, self.__num_samples, self.__total_samples,
               self._destination, time.perf_counter() - start_time))

    @abc.abstractmethod
    def _generate_image(self, ci_si: Tuple[int, int]) -> Tuple[int, int, np.array]:
        pass

    def save_npz(self, file_name: str, test_size: float = .3):
        indexes = np.random.permutation(self.__total_samples)
        x, y = self.__x[indexes], self.__y[indexes]

        test_num = np.int0(self.__total_samples * test_size)
        x_train, y_train = x[:-test_num], y[:-test_num]
        x_test, y_test = x[-test_num:], y[-test_num:]

        np.savez('%s/%s.npz' % (self._destination, file_name),
                 x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test)

    def save_thumbnails(self, examples_per_category: int = 10, scale: float = 1.0, filename: str = 'thumbnails'):
        sample_size = np.int0(np.multiply(self._image_size, scale))
        thumbnail_size = np.int0(np.multiply((examples_per_category, self.__num_categories), sample_size))
        thumbnail_image = Image.new('RGB', tuple(thumbnail_size))

        for category_idx in range(self.__num_categories):
            for i in range(examples_per_category):
                sample_idx = np.random.randint(0, self.__num_samples)
                dataset_idx = self._get_image_idx(category_idx, sample_idx)
                resized_sample = cv2.resize(self.__x[dataset_idx], tuple(sample_size))
                sample_image = Image.fromarray(255 - resized_sample)

                sample_position = (sample_size[0] * i, sample_size[1] * category_idx)
                thumbnail_image.paste(sample_image, sample_position)

        thumbnail_image.save('%s/%s.png' % (self._destination, filename))
