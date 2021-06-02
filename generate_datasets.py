from examples.simple_dataset_3 import SimpleDataset3

image_size = 28, 28
samples_per_category = 1000
destination = "./output"

if __name__ == "__main__":
    # for dataset_cls in (SimpleDataset, RoundDataset, ThreeSixtyDataset):
    dataset = SimpleDataset3(samples_per_category, image_size, destination, save_images=False)
    dataset.generate()
    dataset.save_npz()
    dataset.save_thumbnails(10, 2)
