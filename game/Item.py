import os
import pygame  # pygame is used for loading images

class Item:
    def __init__(self, image, position, tile_size):
        """
        Initialize the item with an image, position, and tile size.
        """
        if not isinstance(image, pygame.Surface):
            raise TypeError("Image must be a valid Pygame Surface object.")
        
        if not isinstance(position, tuple) or len(position) != 2:
            raise ValueError("Position must be a tuple with two values (x, y).")
        
        self.image = pygame.transform.scale(image, (tile_size, tile_size))  # Handle resizing here
        self.position = position
        self.tile_size = tile_size


    def get_position(self):
        """
        Get the current position of the item.
        
        :return: The (row, col) position of the item.
        """
        return self.position

    def set_position(self, position, maze):
        """
        Set a new position for the item and ensure it's valid within the maze layout.
        
        :param position: The new (row, col) position of the item.
        :param maze: The Maze object to validate the position against.
        """
        if not isinstance(position, tuple) or len(position) != 2:
            raise ValueError("Position must be a tuple with two values (row, col).")

        # Validate the position in the maze before setting it
        if maze.is_valid_position(position):
            self.position = position
            print(f"Item placed at valid position: {self.position}")
        else:
            print(f"Attempted to place item at invalid position: {position}")
            raise ValueError(f"Invalid position: {position} is not valid in the maze layout.")

        def draw(self, screen):
            """
            Draw the item on the screen if its position is valid.
            """
            if self.position and len(self.position) == 2 and self.position != (None, None):
                x, y = self.position
                screen.blit(self.image, (x * self.tile_size, y * self.tile_size))  # Apply tile size scaling
            else:
                print(f"Skipping item with invalid position: {self.position}")

