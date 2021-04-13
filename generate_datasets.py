from dataset.round_dataset import RoundDataset
from dataset.simple_dataset import SimpleDataset
from dataset.threesixty_dataset import ThreeSixtyDataset

image_size = 28, 28
samples_per_category = 10
destination = "./output/simple"

if __name__ == "__main__":
    dataset = ThreeSixtyDataset(samples_per_category, image_size, destination, save_images=False)
    dataset.generate()
    dataset.save_npz()
    dataset.save_thumbnails(10, 2)
