import random



class NPC:
    def __init__(self, image, position, tile_size, maze=None):
  
        self.image = image
        self.position = position if position else (0, 0)  # Fallback to (0, 0) if no position provided
        self.tile_size = tile_size
        self.maze = maze


    def move(self, maze):
        """
        Move the NPC in a random direction, checking maze boundaries.
        :param maze: The maze instance to check valid positions.
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
        if maze.is_valid_position(tuple(new_position)):
            self.position = tuple(new_position)
        else:
            print(f"NPC tried to move at {direction}. Blocked at {new_position}.")
    def is_move_valid(self, new_position):
   
        return self.maze.is_valid_position(new_position) if self.maze else False

    def draw(self, screen):
   
        screen.blit(self.image, (self.position[1] * self.tile_size, self.position[0] * self.tile_size))

    
