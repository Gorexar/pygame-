import pygame
import sys
import os
print("Files in mazes directory:", os.listdir("C:/Users/gorex/Desktop/pygame!/mazes/"))
import random
import json
#main game logic
class AssetLoader:
    def __init__(self, image_dir):
        self.image_dir = image_dir
        self.images = {}
    def load_images(self):
        self.images["background"] = pygame.image.load(os.path.join(self.image_dir, "backgrounds/background_image_light.png"))
        self.images["player"] = pygame.image.load(os.path.join(self.image_dir, "sprites/cat.png"))
        self.images["npc"] = pygame.image.load(os.path.join(self.image_dir, "sprites/wolf.png"))
        # Load other images similarly
    def load_all(self):
        self.load_images()
class Maze:
    def __init__(self, layout, player_position, npc_positions, item_positions):
        self.layout = layout
        self.player_position = player_position
        self.npc_positions = npc_positions
        self.item_positions = item_positions

    @classmethod
    def load_from_file(cls, file_path):
        try:
            with open(file_path, 'r') as f:
                maze_data = json.load(f)
            
            # Validate the loaded data
            required_keys = ["layout", "player_position", "npc_positions", "item_positions"]
            if not all(key in maze_data for key in required_keys):
                raise ValueError("Maze data is missing required keys.")
            
            layout = maze_data["layout"]
            player_position = maze_data["player_position"]
            npc_positions = maze_data["npc_positions"]
            item_positions = maze_data["item_positions"]
            
            return cls(layout, player_position, npc_positions, item_positions)
        
        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            print(f"Error loading maze from {file_path}: {e}")
            return None  # or raise an exception, depending on your error handling strategy

    def get_valid_positions(self):
        """Return a list of valid positions (not walls or obstacles)"""
        valid_positions = []
        for row in range(len(self.layout)):
            for col in range(len(self.layout[row])):
                if self.layout[row][col] == 0:  # Assuming 0 represents a walkable path
                    valid_positions.append([row, col])
        return valid_positions
    def is_valid_position(self, position):
        return self.current_maze.is_valid_position(position)  # Use the maze's method
        # Check if the position is within bounds and if it's a path (1)
    def generate_items(self, items):
        print("Generating items...")
        """Place items in predefined or random valid locations."""
        valid_positions = self.get_valid_positions()
        
        for item in items.values():  # Iterate directly over the item objects
            if item.get_item_position() is None:  # Check if the item has no position
                random_pos = random.choice(valid_positions)
                valid_positions.remove(random_pos)
                item.set_position(random_pos)  # Set the item's position
        
        return items

    print("Finished generating items.")
class Item:
    def __init__(self, position):
        self.position = position

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position
      
    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position
class item_attributes(Item):
    def __init__(self, item, item_type, item_name, item_value, item_size):
        super().__init__(item.position)  # Ensure to call the parent constructor
        self.item = item
        self.item_type = item_type
        self.item_name = item_name
        self.item_value = item_value
        self.item_size = item_size

    def __str__(self):
        return f"{self.item_name} is a {self.item_type} and weighs {self.item_size} and it's value is {self.item_value}"

    def get_item_position(self):
        return self.item.get_position()
class ConsumableItem(item_attributes):
    def __init__(self, name, description, item_size, item_type, value=None):
        # Create an Item instance with a default position (e.g., None)
        item = Item(position=None)
        
        # Pass all the required parameters to the superclass
        super().__init__(item, item_type, name, value, item_size)
        
        self.value = value  # This is specific to ConsumableItem
Consumeable_items = {
    "food": ConsumableItem(
        name="food",
        description="Heals 10 HP",
        item_size=1,
        item_type="food",
        value=10
    ),
    "tiny scratching post": ConsumableItem(
        name="tiny scratching post",
        description="Sharpens claws a small amount",
        item_size=1,
        item_type="object"
    ),
    "tasty treats": ConsumableItem(
        name="Treats",
        description="tasty treats Heals 50 HP",
        item_size=1,
        item_type="treat",
        value=50
    ),
    "medical treats": ConsumableItem(
        name="medical treats",
        description="Cures poison & bleeding",
        item_size=1,
        item_type="treat"
    ),
    "catnip": ConsumableItem(
        name="catnip",
        description="Makes you feel good +20 HP +5 speed",
        item_size=1,
        item_type="treat",
        value=20
    ),
}
# character management
class Player:
    def __init__(self, position, inventory_size=5):
        self.position = position
        self.inventory = []
        self.inventory_size = inventory_size

    def move(self, direction, maze):
        row, col = self.position
        if direction == pygame.K_LEFT:
            new_position = (row, col - 1)
        elif direction == pygame.K_RIGHT:
            new_position = (row, col + 1)
        elif direction == pygame.K_UP:
            new_position = (row - 1, col)
        elif direction == pygame.K_DOWN:
            new_position = (row + 1, col)
        else:
            return

        if maze.is_valid_position(new_position):
            self.position = new_position
#npc managment
class NPC:
    def __init__(self, position, maze):
        self.position = position
        self.maze = maze
        self.speed = 3  # You can adjust speed as needed

    def move(self):
        # Example logic for random movement
        possible_directions = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
        direction = random.choice(possible_directions)
        
        new_position = self.position[:]
        
        if direction == pygame.K_LEFT:
            new_position[1] -= 1
        elif direction == pygame.K_RIGHT:
            new_position[1] += 1
        elif direction == pygame.K_UP:
            new_position[0] -= 1
        elif direction == pygame.K_DOWN:
            new_position[0] += 1
            new_position[0] += 1
        
        # Check if the new position is valid before updating
        if self.is_move_valid(new_position):
            self.position = new_position

    def is_move_valid(self, new_position):
        return self.maze.is_valid_position(new_position)  # Call the maze's method to check validity 

    def is_valid_position(self, position):
        row, col = position
        # Check if the position is within bounds and if it's a path (1)
        return (0 <= row < len(self.layout) and 
                0 <= col < len(self.layout[0]) and 
                self.layout[row][col] == 1)

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
#action magment
class Actions:

    def __init__(self, player, item):
        self.player = player
        self.item = item

    def player_pickup_item(self):
        if self.player.position == self.item.position:
            if not self.player.is_inventory_full():
                self.player.add_to_inventory(self.item)  # Add item to player's inventory
                self.item.position = None  # Remove item from the game
                print("You picked up the item!")
            else:
                print("Inventory full")

    def is_move_valid(self, new_row, new_col, maze):
        num_rows = len(maze)
        num_cols = len(maze[0])
        valid = True

        # Check if the new row is outside play space
        if new_row < 0 or new_row >= num_rows:
            valid = False

        # Check if the new column is out of play space
        if new_col < 0 or new_col >= num_cols:
            valid = False

        # Check if the new position is a wall
        if valid:  # Only check for walls if bounds are okay
            if maze[new_row][new_col] == 3 or maze[new_row][new_col] == 5:
                valid = False

        # Return the validity status
        return valid

class Game:
     
    def __init__(self):
        self.asset_loader = AssetLoader("images")
        self.asset_loader.load_all()
        self.images = self.asset_loader.images
        
        # Game settings
        self.settings = {
            "health": 5,
            "npc_speed": 3,
            "tile_size": 50,
            "damage": 5,
            "player_speed": 3,

            # Add more settings as needed
        }
        self.state = "PLAYING" # Set initial state

        # Initialize player and NPC positions
        self.player_positions = []  # Initialize player_positions
        self.npc_positions = []     # Initialize npc_positions

    def initialize_game(self):
        self.WIDTH, self.HEIGHT = 1250, 1250
        self.tile_size = 50
        self.image_dir = "images"
        self.images = self.initialize_images()  # Ensure this method is defined
        self.resize_images(self.images, self.tile_size, self.WIDTH, self.HEIGHT)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Maze Game for Anastazja!") 
        self.icon = self.images["player"]
        self.game_over = False
        self.game_win = False
        self.current_maze = maze
        self.state = "PLAYING"  # Set initial state
        #self.inventory = []#

        directory_path = "mazes"  # Adjust this to your directory
        self.mazes, self.player_positions, self.item_positions, self.npc_positions = self.load_mazes_from_directory(directory_path)
        # Optionally handle if no mazes were loaded
        if not self.mazes:
            print("No maze loaded.")
            return  # Handle appropriately

        # Initialize player and NPCs
        self.current_maze_index = 0  # Start with the first maze
        self.current_maze = Maze(self.mazes[self.current_maze_index], self.player_positions[self.current_maze_index], self.npc_positions[self.current_maze_index], self.item_positions[self.current_maze_index])
        self.player_position = self.player_positions[self.current_maze_index]
        self.npc_positions = self.npc_positions[self.current_maze_index]
        self.player = Player(self.player_position)
        self.npcs = [NPC(position=pos, maze=self.current_maze) for pos in self.npc_positions]  # Initialize npcs attribute
        print("Initializing game...")
        print("NPC positions:", self.npc_positions)
        print("Maze:", self.current_maze)
    def initialize_images(self):
            # Load and return images
            images = {
                "player": pygame.image.load(os.path.join(self.image_dir, "player.png")),
                "npc": pygame.image.load(os.path.join(self.image_dir, "npc.png")),
                "path": pygame.image.load(os.path.join(self.image_dir, "path.png")),
                "wall": pygame.image.load(os.path.join(self.image_dir, "wall.png")),
                # Add more images as needed
            }
            return images
    
    def resize_images(self, images, tile_size, width, height):
            for key in images:
                images[key] = pygame.transform.scale(images[key], (tile_size, tile_size))   
                images["path"] = pygame.transform.scale(images["path"], (tile_size, tile_size))
                images["wall"] = pygame.transform.scale(images["wall"], (tile_size, tile_size))
                images["goal"] = pygame.transform.scale(images["goal"], (tile_size, tile_size))
                images["border"] = pygame.transform.scale(images["border"], (tile_size, tile_size))
                images["player"] = pygame.transform.scale(images["player"], (tile_size, tile_size))
                images["npc"] = pygame.transform.scale(images["npc"], (tile_size, tile_size))
                images["item"] = pygame.transform.scale(images["item"], (tile_size, tile_size))
                images["background"] = pygame.transform.scale(images["background"], (width, height))
            
            
    
    def load_mazes_from_directory(self, directory_path):
        mazes = []
        player_positions = []
        item_positions = []
        npc_positions = []

        for file_name in os.listdir(directory_path):
            if file_name.endswith('.json'):
                maze_path = os.path.join(directory_path, file_name)
                maze_instance = Maze.load_from_file(maze_path)
                if maze_instance:
                    mazes.append(maze_instance.layout)
                    player_positions.append(maze_instance.player_position)
                    item_positions.append(maze_instance.item_positions)
                    npc_positions.append(maze_instance.npc_positions)
        return mazes, player_positions, item_positions, npc_positions
    
    def draw_maze(self):
        if not hasattr(self, 'current_maze') or self.current_maze is None:
            print("Error: current_maze is not initialized.")
            return

        for row in range(len(self.current_maze.layout)):
            for col in range(len(self.current_maze.layout[row])):
                tile_value = self.current_maze.layout[row][col]
                if tile_value == 1:  # Path
                    self.screen.blit(self.images["path"], (col * self.tile_size, row * self.tile_size))
                elif tile_value == 3:  # Wall
                    self.screen.blit(self.images["wall"], (col * self.tile_size, row * self.tile_size))
                # Add more conditions for other elements if needed, like goal or border

    def get_random_position(self, value):
        print(type(self.current_maze))  # Should be <class '__main__.Maze'>
        valid_positions = [(x, y) for x in range(len(self.current_maze.layout)) 
                        for y in range(len(self.current_maze.layout[0]))
                        if self.current_maze.layout[x][y] == value]
        return random.choice(valid_positions) if valid_positions else None

    def reset_player_and_npcs(self):
        """Reset player and NPC positions."""
        self.player_positions = self.get_random_position(1)  # Update the player position
        self.npc_positions = [self.get_random_position(1) for _ in range(4)]  # Update NPC positions
        self.player.position = self.player_positions  # Set player to new position

# Initialize the game

    def display_game_over(self):
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over! Press any key to restart.", True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        self.screen.blit(self.images["background"], (0, 0))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

    def display_game_win(self):
        font = pygame.font.Font(None, 74)
        text = font.render("You Win! Press any key to restart.", True, (0, 255, 0))
        text_rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        self.screen.blit(self.images["background"], (0, 0))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

    def move(self, direction):
        row, col = self.position
        new_position = [row, col]

        if direction == pygame.K_LEFT:
            new_position[1] -= 1
        elif direction == pygame.K_RIGHT:
            new_position[1] += 1
        elif direction == pygame.K_UP:
            new_position[0] -= 1
        elif direction == pygame.K_DOWN:
            new_position[0] += 1

        if self.is_move_valid(new_position[0], new_position[1]):
            self.position = new_position

    def add_to_inventory(self, item):
        if len(self.inventory) < self.inventory_size:
            self.inventory.append(item)
            return True
        else:
            return False

    def restart_game(self):
        self.initialize_game()  # Reset game state
        self.state = "PLAYING"
    def update_game(self):
            for npc in self.npcs:
                npc.move()
                # self.check_game_state()  # Move each NPC 
            # # Example check for win/lose conditions
            # if self.player.health <= 0:
            #     self.game_over = True
            # elif self.player.position == self.mazes[0].goal_position:  # Assuming you have a goal position
            #     self.game_win = True
        
    
    def load_maze(self, maze_file):
        file_path = os.path.join("mazes", maze_file)
        maze = Maze.load_from_file("mazes/maze_1.json")
        pygame.display.flip()
        if maze:
            self.current_maze = maze  # Set the current maze here

            # Validate player position
            if not self.is_valid_position(maze.player_position):
                print(f"Invalid player position: {maze.player_position}. Resetting to default.")
                self.player_position = self.get_random_position(1)  # Set to a valid position
            else:
                self.player_position = maze.player_position

            # Validate NPC positions
            self.npc_positions = []
            for npc_pos in maze.npc_positions:
                if self.is_valid_position(npc_pos):
                    self.npc_positions.append(npc_pos)
                else:
                    print(f"Invalid NPC position: {npc_pos}. Resetting to random position.")
                    self.npc_positions.append(self.get_random_position(1))  # Set to a valid position

            # Validate item positions
            self.item_positions = []
            for item_pos in maze.item_positions:
                if self.is_valid_position(item_pos):
                    self.item_positions.append(item_pos)
                else:
                    print(f"Invalid item position: {item_pos}. Resetting to random position.")
                    self.item_positions.append(self.get_random_position(1))  # Set to a valid position

            self.reset_player_and_npcs()  # Reset player and NPCs based on loaded maze

        else:
            print(f"Error loading maze from {file_path}")

        # Handle game states
        if self.state == "PLAYING":
            keys = pygame.key.get_pressed()  # Get the current state of all keys
            direction = None
            
            if keys[pygame.K_LEFT]:
                direction = pygame.K_LEFT
            elif keys[pygame.K_RIGHT]:
                direction = pygame.K_RIGHT
            elif keys[pygame.K_UP]:
                direction = pygame.K_UP
            elif keys[pygame.K_DOWN]:
                direction = pygame.K_DOWN
            
            if direction:  # If there's a valid direction input
                action = Actions(self.player, None)  # Create an Actions instance
                new_row, new_col = self.player.position

                if direction == pygame.K_LEFT:
                    new_col -= 1
                elif direction == pygame.K_RIGHT:
                    new_col += 1
                elif direction == pygame.K_UP:
                    new_row -= 1
                elif direction == pygame.K_DOWN:
                    new_row += 1

                # Check if the move is valid before updating the player position
                if action.is_move_valid(new_row, new_col, self.current_maze.layout):
                    self.player.move(direction)  # Update player position if valid
            
            self.render()  # Render the game visuals
            self.clock.tick(30)  # Control the frame rate

        elif self.state == "GAME_OVER":
            self.display_game_over()
            self.wait_for_keypress()
        elif self.state == "GAME_WIN":
            self.display_game_win()
            self.wait_for_keypress()

    def handle_events(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if self.state in ("GAME_OVER", "GAME_WIN"):
                        self.restart_game()
                        pygame.display.flip()  # Restart game on key press
                    elif self.state == "PLAYING":
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                        elif event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                            self.player.move(event.key)  # Call the move method of the Player class

    # def check_game_state(self):
    #     if self.player.health <= 0:
    #         self.state = "GAME_OVER"
    #     elif self.player.position == self.current_maze.goal_position:  # Adjust this to your actual goal position
            self.state = "GAME_WIN"

    def wait_for_keypress(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    waiting = False
                    self.restart_game()  # Restart game after key press

#renders the game
    def render(self):
        self.screen.blit(self.images["background"], (0, 0))
        self.draw_maze()  # Draw the maze
        self.draw_player()
        self.draw_npcs()
        self.draw_items()
        pygame.display.flip()

    def reset_player_and_npcs(self):
            self.player = Player(position=self.player_positions, inventory_size=5)
            self.npcs = [NPC(position=pos, maze=self.current_maze) for pos in self.npc_positions]
    
    def initialize_images(self):
         return {
             "path": pygame.image.load(os.path.join(self.image_dir, 'sprites/path_image.png')),
             "wall": pygame.image.load(os.path.join(self.image_dir, 'sprites/grass2.png')),
             "goal": pygame.image.load(os.path.join(self.image_dir, 'sprites/goal.png')),
             "border": pygame.image.load(os.path.join(self.image_dir, 'sprites/locust_tree.png')),
             "player": pygame.image.load(os.path.join(self.image_dir, 'sprites/cat.png')),
             "npc": pygame.image.load(os.path.join(self.image_dir, 'sprites/wolf.png')),
             "item": pygame.image.load(os.path.join(self.image_dir, 'sprites/goal.png')),
             "background": pygame.image.load(os.path.join(self.image_dir, 'backgrounds/background_image_light.png'))
         }

    
    def main_loop(self):
        running = True
        while running:
            self.handle_events()
            self.update_game()
            self.render()
            pygame.display.flip()
            self.clock.tick(60)
            self.initialize_game()
            
            
if __name__ == "__main__":
    maze = Maze.load_from_file("mazes/maze_1.json")
    if maze:
        print("Maze loaded successfully.")
        print("Player Position:", maze.player_position)
        print("NPC Positions:", maze.npc_positions)
        print("Item Positions:", maze.item_positions)
        pygame.init()
        game = Game()  # Create an instance of your game
        game.main_loop()  # Start the game loop
