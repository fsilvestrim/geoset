from dataset.simple_dataset import SimpleDataset

image_size = 28, 28
samples_per_category = 100
destination = "./output/simple"

if __name__ == "__main__":
    dataset = SimpleDataset(samples_per_category, image_size, destination, save_images=False)
    dataset.generate()
    dataset.save_npz("simple")
    dataset.save_thumbnails(10, 2)
