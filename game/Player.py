import os
import pygame  # pygame is used for loading images

class Player:
    def __init__(self, image, position, tile_size):
      
        self.image = image  # The player's image
        self.position = position  # The player's position (row, col) in the grid
        self.tile_size = tile_size  # Size of each tile in pixels

    def draw(self, screen):
        """
        Draws the player on the given screen.
        Args:
            screen (pygame.Surface): The surface on which the player will be drawn.
        """
        
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
