import pygame

class Item:
    def __init__(self, image, position, tile_size):
        """
        Initialize the item with an image, position, and tile size.
        
        :param image: The image representing the item.
        :param position: The (x, y) position of the item in the maze.
        :param tile_size: The size of each tile in the maze.
        """
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
        self.position = position

    def draw(self, screen):
        """
        Draw the item on the screen at its position.
        
        :param screen: The Pygame screen surface to draw the item on.
        """
        x, y = self.position
        screen.blit(self.image, (x * self.tile_size, y * self.tile_size))