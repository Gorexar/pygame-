#npc.py
import random
import pygame
from Actions    import Actions


class NPC:
    def __init__(self, image, position, tile_size, maze):
        self.image = image
        self.position = tuple(position) if isinstance(position, list) else position
        self.tile_size = tile_size
        self.maze = maze
        self.health = 50  # NPC's starting health
        self.max_health = 50  # NPC's maximum health
        self.is_alive = True  # Is the NPC alive?
        self.move_delay = 2500  # Delay between NPC moves in milliseconds (50 seconds)
        self.last_move_time = pygame.time.get_ticks()
        self.rect = pygame.Rect(self.position[1] * self.tile_size, self.position[0] * self.tile_size, tile_size, tile_size)

    def set_position(self, position):
        """Set the position of the NPC."""
        self.position = position

    def move(self, maze):
        """Move the NPC after a delay, ensuring it moves only to valid positions."""
        # Ensure the current position is valid before moving
        if self.position is None or None in self.position:
            print(f"NPC has invalid position: {self.position}. Skipping move.")
            return  # Skip movement if the position is invalid

        current_time = pygame.time.get_ticks()

        # Check if enough time has passed for the NPC to move
        if current_time - self.last_move_time < self.move_delay:
            return  # Not enough time has passed, skip this move cycle

        new_position = list(self.position)

        # Random movement logic (up, down, left, right)
        direction = random.choice(["up", "down", "left", "right"])
        if direction == "up":
            new_position[0] -= 1
        elif direction == "down":
            new_position[0] += 1
        elif direction == "left":
            new_position[1] -= 1
        elif direction == "right":
            new_position[1] += 1

        # Check if the new position is valid in the maze before updating
        if maze.is_valid_position(tuple(new_position)):
            self.position = tuple(new_position)
            self.last_move_time = current_time  # Update the last move time
            self.rect.topleft = (self.position[1] * self.tile_size, self.position[0] * self.tile_size)
        else:
            print(f"NPC cannot move to invalid position: {new_position}")


    def is_move_valid(self, new_position):
   
        return self.maze.is_valid_position(new_position) if self.maze else False

    def draw(self, screen):
        """
        Draw the npc on the screen if its position is valid.
        """
        if self.position and len(self.position) == 2 and self.position != (None, None):
            x, y = self.position
            screen.blit(self.image, (y * self.tile_size, x * self.tile_size))  # Note: x, y order (row, col)
        else:
            print(f"Skipping npc with invalid position: {self.position}")

    def take_damage(self, amount):
        """
        Reduces the NPC's health by the given amount.
        
        :param amount: Amount of damage to take.
        """
        if self.is_alive:
            self.health -= amount
            print(f"NPC takes {amount} damage! Current health: {self.health}")
            if self.health <= 0:
                self.health = 0
                self.die()
    def die(self):
        """
        Handle NPC death.
        """
        print("NPC has died.")
        self.is_alive = False
        self.rect = None  # Remove the rect so it no longer collides