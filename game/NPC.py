import random
import pygame
class NPC:
    def __init__(self, image, position, tile_size, maze):
        """
        Initialize the NPC with basic attributes.
        
        :param image: The NPC's image (pygame.Surface).
        :param position: The NPC's position (row, col) in the grid.
        :param tile_size: Size of each tile in pixels.
        :param maze: The reference to the maze for movement logic.
        """
        self.image = image
        self.position = tuple(position) if isinstance(position, list) else position  # Ensure it's a tuple
        self.tile_size = tile_size
        self.maze = maze
        
        # Movement settings
        self.move_delay = 1000  # Delay in milliseconds between moves
        self.last_move_time = pygame.time.get_ticks()  # Time since last move
        
        # Health attributes
        self.health = 50  # NPC's starting health
        self.max_health = 50  # NPC's maximum health
        self.is_alive = True  # Is the NPC alive?
        
        # Create a pygame.Rect for collision detection
        self.rect = pygame.Rect(self.position[1] * tile_size, self.position[0] * tile_size, tile_size, tile_size)

    def move(self):
        """
        Move the NPC in a way defined by the game logic.
        The movement could be random, follow the player, or any other pattern.
        """
        current_time = pygame.time.get_ticks()
        
        # Only move if the delay time has passed
        if current_time - self.last_move_time > self.move_delay:
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Possible directions: Right, Left, Down, Up
            random.shuffle(directions)  # Shuffle the directions for randomness

            for direction in directions:
                new_position = (self.position[0] + direction[0], self.position[1] + direction[1])
                
                # Check if the new position is valid in the maze
                if self.maze.is_valid_position(new_position):
                    # Update position
                    self.position = new_position
                    # Update the rect for collision detection
                    self.rect.topleft = (self.position[1] * self.tile_size, self.position[0] * self.tile_size)
                    self.last_move_time = current_time  # Reset the move timer
                    break  # Move only once per cycle

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
        Handle NPC's death.
        """
        self.is_alive = False
        print("NPC has died!")

    def draw(self, screen):
        """
        Draw the NPC on the screen at its current position.
        
        :param screen: The screen surface to draw the NPC on.
        """
        x, y = self.position[1] * self.tile_size, self.position[0] * self.tile_size
        screen.blit(self.image, (x, y))  # Draw the NPC's image at the calculated position
