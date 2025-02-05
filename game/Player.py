#player.py
import os
from AssetLoader import AssetLoader
import pygame  # pygame is used for loading images
from Actions import Actions  # Import the Actions class
class Player:
    def __init__(self, image, position, tile_size):
      
        self.image = image  # The player's image
        self.original_image = image
        self.position = position  # The player's position (row, col) in the grid
        self.tile_size = tile_size  # Size of each tile in pixels
        self.health = 100  # Player's health
        self.is_alive = True
        self.can_take_damage = True
        self.rect = pygame.Rect(self.position[1] * self.tile_size, self.position[0] * self.tile_size, tile_size, tile_size)
    def draw(self, screen):

        screen.blit(self.image, (self.position[1] * self.tile_size, self.position[0] * self.tile_size))

    def move(self, direction, maze):
 
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
            self.rect.topleft = (self.position[1] * self.tile_size, self.position[0] * self.tile_size)
        else:
            print(f"Player cannot move {direction}. Blocked at {new_position}.")
            
    def take_damage(self, amount):
        """
        Temporarily change player color when taking damage.
        """
        if self.is_alive:
            if self.can_take_damage:  # Only take damage if allowed
                self.health -= amount
                print(f"Player took {amount} damage! Current health: {self.health}")
                pygame.display.update()
                if self.health <= 0:
                    self.health = 0
                    self.die()
            

    def die(self):
        """
        Handle player death.
        """
        print("Player has died. Game over.")
        self.is_alive = False