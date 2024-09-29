# character management
class Player:
    def __init__(self, image, position, tile_size):
        self.image = image  # The player's image
        self.position = position  # The player's position (row, col) in the grid
        self.tile_size = tile_size  # Size of each tile in pixels

    def draw(self, screen):
        """Draw the player on the screen."""
        # Convert grid position to pixel position and blit the image on the screen
        screen.blit(self.image, (self.position[1] * self.tile_size, self.position[0] * self.tile_size))

    
    def move(self, direction, maze):
        """Move the player in the given direction, checking maze boundaries."""
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
            print("Player cannot move there. It's blocked.")
