#npc managment
class NPC:
    def __init__(self, image, position, tile_size, maze=None):
        self.image = image
        self.position = position  # The NPC's position (row, col)
        self.tile_size = tile_size  # Tile size for movement
        self.maze = maze  # Store the maze if needed for pathfinding or logic

    
    def move(self, maze):
        """Move the NPC in a random direction, checking maze boundaries."""
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
            print(f"NPC tried to move {direction}, but was blocked.")

    def is_move_valid(self, new_position):
        return self.maze.is_valid_position(new_position)  # Call the maze's method to check validity 

    def is_valid_position(self, position):
        row, col = position
        # Check if the position is within bounds and if it's a path (1)
        return (0 <= row < len(self.layout) and 
                0 <= col < len(self.layout[0]) and 
                self.layout[row][col] == 1)
    def draw(self, screen):
        """Draw the NPC on the screen."""
        screen.blit(self.image, (self.position[1] * self.tile_size, self.position[0] * self.tile_size))
#what is a player

    def is_inventory_full(self):
        return len(self.inventory) >= self.inventory_size
        #now that self is self, and self knows where self is. let see if self can move self.
    #how does a palyer move
    def add_to_inventory(self, item):
        if len(self.inventory) < self.inventory_size:
            self.inventory.append(item)
            return True
        else:
            return False

    def is_inventory_full(self):
        return len(self.inventory) >= self.inventory_size        

