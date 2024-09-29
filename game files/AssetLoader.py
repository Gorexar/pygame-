import os
import pygame

class AssetLoader:
    def __init__(self, image_dir):
        self.image_dir = image_dir
        self.images = {}

    def load_images(self):
        try:
            self.images["background"] = pygame.image.load(os.path.join(self.image_dir, "backgrounds/background_image_light.png"))
            self.images["player"] = pygame.image.load(os.path.join(self.image_dir, "sprites/cat.png"))
            self.images["npc"] = pygame.image.load(os.path.join(self.image_dir, "sprites/wolf.png"))
            self.images["wall"] = pygame.image.load(os.path.join(self.image_dir, "sprites/wall.png"))
            self.images["border"] = pygame.image.load(os.path.join(self.image_dir, "sprites/border.png"))
            self.images["path"] = pygame.image.load(os.path.join(self.image_dir, "sprites/path.png"))
            self.images["item"] = pygame.image.load(os.path.join(self.image_dir, "sprites/Scraching_post_item.png"))
            # Add more images as needed
        except pygame.error as e:
            print(f"Error loading image: {e}")

    def load_all(self):
        self.load_images()

    def get_image(self, name):
        return self.images.get(name, None)