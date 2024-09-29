import os
import pygame  # pygame is used for loading images

class Player:
    def __init__(self, image, position, tile_size):
        """
        Initialize the Player object with image, position, and tile size.
        
        :param image: The player's image.
        :param position: Tuple (row, col) representing the player's position in the grid.
        :param tile_size: The size of each tile in pixels.
        """
        self.image = image  # The player's image
        self.position = position  # The player's position (row, col) in the grid
        self.tile_size = tile_size  # Size of each tile in pixels

    def draw(self, screen):
        """
        Draw the player on the screen.
        
        :param screen: Pygame screen surface to draw the player on.
        """
        # Convert grid position to pixel position and blit the image on the screen
        screen.blit(self.image, (self.position[1] * self.tile_size, self.position[0] * self.tile_size))

    def move(self, direction, maze):
        """
        Move the player in the given direction, checking maze boundaries.
        
        :param direction: The direction to move ('up', 'down', 'left', 'right').
        :param maze: The maze object, used to validate the move.
        """
        if direction not in ["up", "down", "left", "right"]:
            print(f"Invalid direction: {direction}. Use 'up', 'down', 'left', or 'right'.")
            return

        # Calculate new position based on direction
        new_position = list(self.position)
        
        if direction == "up":
            new_position[0] -= 1
        elif direction == "down":
            new_position[0] += 1
        elif direction == "left":
            new_position[1] -= 1
        elif direction == "right":
            new_position[1] += 1

        # Check if the new position is valid in the maze
        if maze.is_valid_position(tuple(new_position)):
            self.position = tuple(new_position)
        else:
            print(f"Player cannot move {direction}. Blocked at {new_position}.")
