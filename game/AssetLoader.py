import os
import pygame

class AssetLoader:
    def __init__(self, image_dir):
        """
        Initialize the asset loader with the directory where images are stored.
        
        :param image_dir: Directory where images are stored.
        """
        self.image_dir = image_dir
        self.images = {}

    def load_images(self):
        """
        Load images from predefined paths into the images dictionary.
        """
        image_files = {
            "background": "backgrounds/background_image_light.png",
            "player": "sprites/cat.png",
            "npc": "sprites/wolf.png",
            "wall": "sprites/wall.png",
            "border": "sprites/border.png",
            "path": "sprites/path.png",
            "item": "sprites/Scraching_post_item.png"
        }

        for name, file_path in image_files.items():
            full_path = os.path.join(self.image_dir, file_path)
            if os.path.exists(full_path):
                try:
                    self.images[name] = pygame.image.load(full_path)
                    print(f"Successfully loaded {name} from {full_path}")
                except pygame.error as e:
                    print(f"Error loading {name} from {full_path}: {e}")
            else:
                print(f"File not found: {full_path}")

    def load_all(self):
        """
        Load all images into the images dictionary.
        """
        self.load_images()

    def get_image(self, name):
        """
        Retrieve an image from the loaded images by name.
        
        :param name: The name of the image to retrieve.
        :return: The pygame Surface object for the image, or None if not found.
        """
        return self.images.get(name)
