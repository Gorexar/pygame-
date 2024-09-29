import random
import pygame



class NPC:
    def __init__(self, image, position, tile_size, maze):
        self.image = image
        self.position = tuple(position) if isinstance(position, list) else position
        self.tile_size = tile_size
        self.maze = maze
        self.move_delay = 1000
        self.last_move_time = pygame.time.get_ticks()

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

        
