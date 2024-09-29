import random
import os
import pygame  # pygame is used for loading images


class NPC:
    def __init__(self, image, position, tile_size, maze=None, inventory_size=5):
        """
        Initialize the NPC with an image, position, tile size, and optional maze.
        
        :param image: Pygame surface representing the NPC.
        :param position: The NPC's position (row, col) in the grid.
        :param tile_size: The size of each tile in the grid.
        :param maze: The maze the NPC is in (optional).
        :param inventory_size: Maximum size of the NPC's inventory (default is 5).
        """
        self.image = image
        self.position = position
        self.tile_size = tile_size
        self.maze = maze
        self.inventory = []  # Initialize inventory as an empty list
        self.inventory_size = inventory_size  # Allow customization of inventory size

    def move(self):
        """
        Move the NPC in a random direction, checking maze boundaries.
        """
        directions = ["up", "down", "left", "right"]
        direction = random.choice(directions)
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
        if self.maze and self.maze.is_valid_position(tuple(new_position)):
            self.position = tuple(new_position)
            print(f"NPC moved {direction} to {self.position}.")
        else:
            print(f"NPC tried to move {direction}, but was blocked at {tuple(new_position)}.")

    def is_move_valid(self, new_position):
        """
        Check if the NPC's move to a new position is valid within the maze.
        
        :param new_position: Tuple (row, col) representing the new position.
        :return: True if the position is valid, False otherwise.
        """
        return self.maze.is_valid_position(new_position) if self.maze else False

    def draw(self, screen):
        """
        Draw the NPC on the screen.
        
        :param screen: Pygame screen surface to draw the NPC on.
        """
        screen.blit(self.image, (self.position[1] * self.tile_size, self.position[0] * self.tile_size))

    def is_inventory_full(self):
        """
        Check if the NPC's inventory is full.
        
        :return: True if the inventory is full, False otherwise.
        """
        return len(self.inventory) >= self.inventory_size

    def add_to_inventory(self, item):
        """
        Add an item to the NPC's inventory if there is space.
        
        :param item: The item to add to the inventory.
        :return: True if the item was added, False if the inventory is full.
        """
        if not self.is_inventory_full():
            self.inventory.append(item)
            return True
        return False
