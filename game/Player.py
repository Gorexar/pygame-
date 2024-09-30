import os
import pygame  # pygame is used for loading images

class Player:
    def __init__(self, image, position, tile_size):
        self.image = image
        self.position = position  # (row, col) format
        self.tile_size = tile_size
        self.health = 100
        self.is_alive = True
        # Create pygame.Rect for collision detection
        self.rect = pygame.Rect(position[1] * tile_size, position[0] * tile_size, tile_size, tile_size)
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
        self.rect.topleft = (self.position[1] * self.tile_size, self.position[0] * self.tile_size)
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
    def take_damage(self, amount):
        """
        Temporarily change player color when taking damage.
        """
        if self.is_alive:
            self.health -= amount
            print(f"Player took {amount} damage! Current health: {self.health}")
            # Temporary visual cue for damage (change player's color)
            self.image.fill((255, 0, 0))  # Flash red
            pygame.time.delay(200)  # Keep the color for 200 ms
            self.image.fill((255, 255, 255))  # Back to normal color
            if self.health <= 0:
                self.health = 0
                self.die()
    def die(self):
        """
        Handle player death.
        """
        print("Player has died. Game over.")
        self.is_alive = False
    def pick_up_item(self, item):
        """
        Pick up the given item and add it to the player's inventory.
        """
        self.inventory.append(item)
        print(f"Player picked up item: {item.name}")
    def heal(self, amount):
        """
        Heal the player by the given amount.
        
        :param amount: Amount of health to restore.
        """
        if self.is_alive:
            self.health += amount
            if self.health > self.max_health:
                self.health = self.max_health
            print(f"Player heals {amount} health. Current health: {self.health}")
    def draw(self, screen):
        """
        Draw the player on the screen at its current position.
        """
        x, y = self.position[1] * self.tile_size, self.position[0] * self.tile_size
        screen.blit(self.image, (x, y))  # Draw the player's image at the calculated position