import os
import pygame  # pygame is used for loading images

class Item:
    def __init__(self, image, position, tile_size):
        """
        Initialize the item with an image, position, and tile size.
        
        :param image: The image representing the item.
        :param position: The (x, y) position of the item in the maze.
        :param tile_size: The size of each tile in the maze.
        """
        if not isinstance(image, pygame.Surface):
            raise TypeError("Image must be a valid Pygame Surface object.")
        
        if not isinstance(position, tuple) or len(position) != 2:
            raise ValueError("Position must be a tuple with two values (x, y).")
        
        self.image = pygame.transform.scale(image, (tile_size, tile_size))
        self.position = position
        self.tile_size = tile_size

    def get_position(self):
        """
        Get the current position of the item.
        
        :return: The (x, y) position of the item.
        """
        return self.position

    def set_position(self, position):
        """
        Set a new position for the item.
        
        :param position: The new (x, y) position of the item.
        """
        if not isinstance(position, tuple) or len(position) != 2:
            raise ValueError("Position must be a tuple with two values (x, y).")
        self.position = position

    def draw(self, screen):
        """
        Draw the item on the screen if its position is valid.
        """
        if self.position and len(self.position) == 2 and self.position != (None, None):
            x, y = self.position
            screen.blit(self.image, (x * self.tile_size, y * self.tile_size))
        else:
            print(f"Skipping item with invalid position: {self.position}")
