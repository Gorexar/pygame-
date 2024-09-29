import random
import pygame



class NPC:
    def __init__(self, image, position, tile_size, maze=None):
  
        self.image = image
        self.position = tuple(position) if isinstance(position, list) else position  # Ensure position is a tuple 
        self.tile_size = tile_size
        self.maze = maze
        self.move_delay = 1000  # Time between moves in milliseconds (3.5 seconds)
        self.last_move_time = pygame.time.get_ticks()


    def move(self, maze):
        """
        Move the NPC if enough time has passed since the last move.
        """
        current_time = pygame.time.get_ticks() # Get the current time in milliseconds
        if current_time - self.last_move_time >= self.move_delay:
            # Only move if enough time has passed
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
            if maze.is_valid_position(tuple(new_position)):
                self.position = tuple(new_position)
                print(f"NPC moved {direction} to {self.position}.")
            else:
                print(f"NPC tried to move {direction}, but was blocked.")

            # Update the last move time
            self.last_move_time = current_time
    def is_move_valid(self, new_position):
   
        return self.maze.is_valid_position(new_position) if self.maze else False

    def draw(self, screen):
        """
        Draw the NPC on the screen at its current position.
        """
        if self.position and len(self.position) == 2:
            screen.blit(self.image, (self.position[1] * self.tile_size, self.position[0] * self.tile_size))
        else:
            print(f"Invalid NPC position detected: {self.position}")

        
