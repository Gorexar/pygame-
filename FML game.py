## still fix game over and win open/close game restart stuff
## DICTIONARY TIME APPARENTLY WOO! OTHERWISE THE GAME LOOPS AND LOOPS AND LOOPS!
## will be required for any kind of not insanity game-menu or defult settings of any kind without
## an insane amount of repeated code time to remap {} must get IN statements IN the brain.
## DICTONARY;  NOPE CLASS TIME need to refactor the game init__(self): and clases
## Inheritance....... must be nice to get one!.... instead i must use it to code apparently..........


## Self is a dumb lable. it should be isolate or this? or this only. saying something is itself is redundant.
#refrencing something refered to : it's self, as it's self. is weird.



import pygame
import sys
import os
import random
import json

 #class to run the game defaults and game loop i think
    #class Game_Defaults:

class Game:
     def __init__(self):
        self.asset_loader = AssetLoader("images", "sounds", "fonts")
        self.asset_loader.load_all()
        self.images = self.asset_loader.images
        self.sounds = self.asset_loader.sounds
        self.fonts = self.asset_loader.fonts

        # Game settings
        self.settings = {
            "health": 5,
            "npc_speed": 3,
            "tile_size": 50,
            "damage": 5,
            "player_speed": 3,

            # Add more settings as needed
        }

        self.initialize_game()

     def initialize_game(self):  
        self.WIDTH, self.HEIGHT = 1250, 1250
        self.tile_size = 50
        self.image_dir = "images"
        self.images = self.initialize_images()
        self.resize_images(self.images, self.tile_size, self.WIDTH, self.HEIGHT)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Maze Game for Anastazja!") 
        self.icon = self.images["player"]
        self.game_over = False
        self.game_win = False
        self.state = "PLAYING"
        self.reset_player_and_npcs()  # New method to reset player and NPCs
        
        game_loc_dir = os.path.dirname(__file__)
        directory_path = os.path.join(game_loc_dir, "mazes")
        self.mazes, self.player_positions, self.item_positions, self.npc_positions = self.load_mazes_from_directory(directory_path)
        
        self.player = Player(position=self.player_positions[0], inventory_size=5)  # Set player position and inventory size
        self.npcs = [NPC(position=pos, maze=self.mazes[0]) for pos in self.npc_positions[0]]  # Ensure using the first maze
        self.items_in_game = self.mazes[0].generate_items(Consumable_items)  # Adjust as needed
     
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


     def restart_game(self):
        self.initialize_game()  # Reset game state
        self.state = "PLAYING"
     def update_game(self):
    # Example check for win/lose conditions
        if self.player.health <= 0:
            self.game_over = True
        elif self.player.position == self.mazes[0].goal_position:  # Assuming you have a goal position
            self.game_win = True
    
     def main_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if self.game_over or self.game_win:
                        self.restart_game()  # Restart game on key press
            if not self.game_over and not self.game_win:
                for npc in self.npcs:
                    npc.move()  # Update NPC positions
                    self.check_game_state()  # Check if the game has ended
                    self.render()  # Render game elements
                    self.clock.tick(30)
     def check_game_state(self):
        if self.game_over:
            self.display_game_over()
            self.wait_for_keypress()
        elif self.game_win:
            self.display_game_win()
            self.wait_for_keypress()

        def wait_for_keypress(self):
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        waiting = False
                        self.restart_game()
#renders the game
     def render(self):
        self.screen.blit(self.images["background"], (0, 0))
        self.draw_player()
        self.draw_npcs()
        self.draw_items()


     def load_mazes_from_directory(self, directory_path):
        mazes = []
        for file_name in os.listdir(directory_path):
            maze = Maze.load_from_file(os.path.join(directory_path, file_name))
            mazes.append(maze)
        
            # Extracting player, item, and NPC positions from the maze instances
            player_positions = [maze.player_position for maze in mazes]
            item_positions = [maze.item_positions for maze in mazes]
            npc_positions = [maze.npc_positions for maze in mazes]
            return mazes, player_positions, item_positions, npc_positions
     
     def initialize_images(self):
         return {
             "path": pygame.image.load(os.path.join(self.image_dir, 'path_image.png')),
             "wall": pygame.image.load(os.path.join(self.image_dir, 'grass2.png')),
             "goal": pygame.image.load(os.path.join(self.image_dir, 'goal.png')),
             "border": pygame.image.load(os.path.join(self.image_dir, 'locust_tree.png')),
             "player": pygame.image.load(os.path.join(self.image_dir, 'cat.png')),
             "npc": pygame.image.load(os.path.join(self.image_dir, 'wolf.png')),
             "item": pygame.image.load(os.path.join(self.image_dir, 'goal.png')),
             "background": pygame.image.load(os.path.join(self.image_dir, 'background_image_light.png'))
         }

     def resize_images(self, images, tile_size, width, height):
         images["path"] = pygame.transform.scale(images["path"], (tile_size, tile_size))
         images["wall"] = pygame.transform.scale(images["wall"], (tile_size, tile_size))
         images["goal"] = pygame.transform.scale(images["goal"], (tile_size, tile_size))
         images["border"] = pygame.transform.scale(images["border"], (tile_size, tile_size))
         images["player"] = pygame.transform.scale(images["player"], (tile_size, tile_size))
         images["npc"] = pygame.transform.scale(images["npc"], (tile_size, tile_size))
         images["item"] = pygame.transform.scale(images["item"], (tile_size, tile_size))
         images["background"] = pygame.transform.scale(images["background"], (width, height))
class AssetLoader:
    def __init__(self, image_dir, sound_dir, font_dir):
        self.image_dir = image_dir
        self.sound_dir = sound_dir
        self.font_dir = font_dir
        self.images = {}
        self.sounds = {}
        self.fonts = {}

    def load_images(self):
        self.images["background"] = pygame.image.load(os.path.join(self.image_dir, "backgrounds/background_image_light.png"))
        self.images["player"] = pygame.image.load(os.path.join(self.image_dir, "sprites/cat.png"))
        self.images["npc"] = pygame.image.load(os.path.join(self.image_dir, "sprites/wolf.png"))
        # Load other images similarly

    def load_sounds(self):
        self.sounds["music"] = pygame.mixer.Sound(os.path.join(self.sound_dir, "music/background_music.wav"))
        self.sounds["effect"] = pygame.mixer.Sound(os.path.join(self.sound_dir, "effects/effect_sound.wav"))
        # Load other sounds similarly

    def load_fonts(self):
        self.fonts["default"] = pygame.font.Font(os.path.join(self.font_dir, "default_font.ttf"), 36)
        # Load other fonts similarly

    def load_all(self):
        self.load_images()
        self.load_sounds()
        self.load_fonts()
    
    
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

    def generate_items(self, items):
        """Place items in predefined or random valid locations"""
        valid_positions = self.get_valid_positions()
        for item_data in items:
            if "position" not in item_data:
                # Randomize item placement if no predefined position
                random_pos = random.choice(valid_positions)
                valid_positions.remove(random_pos)
                item_data["position"] = random_pos
        return items


#is running
class NPC:
    def __init__(self, position, maze):
        self.position = position
        self.maze = maze  

    

#what is a player
class Player:
    def __init__(self, position, inventory_size=5):
        self.position = position
        self.inventory = []
        self.inventory_size = inventory_size

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

    def is_inventory_full(self):
        return len(self.inventory) >= self.inventory_size
        #now that self is self, and self knows where self is. let see if self can move self.
    #how does a palyer move
    def move(self, direction):
        row, col = self.position
        if direction == pygame.K_LEFT:
            self.position = [row, col - 1]
        elif direction == pygame.K_RIGHT:
            self.position = [row, col + 1]
        elif direction == pygame.K_UP:
            self.position = [row - 1, col]
        elif direction == pygame.K_DOWN:
            self.position = [row + 1, col]

    def add_to_inventory(self, item):
        if len(self.inventory) < self.inventory_size:
            self.inventory.append(item)
            return True
        else:
            return False

    def is_inventory_full(self):
        return len(self.inventory) >= self.inventory_size        
# for making an item i need to define what paramters(values)atributes w/e im using for the item in the self (self): part
# had to go deeper and deaper into what is a thing.
class Item:
    def __init__(self, position):
        self.position = position

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position
#atributes of the item
class item_attributes(Item):
    def __init__(self, item, item_type, item_name, item_value, item_weight):
        self.item = item  # Reference to an Item instance
        self.item_type = item_type  # Will categorize the item
        self.item_name = item_name  # Name of the item
        self.item_weight = item_weight  # Will use weight for inventory management
        self.item_value = item_value

    def __str__(self):
        return f"{self.item_name} is a {self.item_type} and weighs {self.item_weight} and it's value is {self.item_value}"

    def get_item_position(self):
        return self.item.get_position()
#atributes of the consumable itesm defined
class ConsumableItem(item_attributes):
    def __init__(self, name, description, weight, item_type, value=None):
        super().__init__(name, description, weight, item_type)
        self.value = value  #value is the amount the item heals or buffs the player
Consumeable_items = {
    "food": ConsumableItem(
        name="food",
        description="Heals 10 HP",
        weight=1,
        item_type="food",
        value=10
    ),
    "tiny scratching post": ConsumableItem(
        name="tiny scratching post",
        description="Sharpens claws a small amount",
        weight=1,
        item_type="object"
    ),
    "tasty treats": ConsumableItem(
        name="Treats",
        description="tasty treats Heals 50 HP",
        weight=1,
        item_type="treat",
        value=50
    ),
    "medical treats": ConsumableItem(
        name="medical treats",
        description="Cures poison & bleeding",
        weight=1,
        item_type="treat"
    ),
    "catnip": ConsumableItem(
        name="catnip",
        description="Makes you feel good +20 HP +5 speed",
        weight=1,
        item_type="treat",
        value=20
    ),
}
#class objects: #(the bunny)
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
        else:print("inventory full")
    #is move valid
    def is_move_valid(new_row, new_col):
        num_rows = 25
        num_cols = 25
        valid = True

        # Check if the new row is outside play space
        if new_row < 0 or new_row >= num_rows:
            valid = False

        # Check if the new column out of play space
        if new_col < 0 or new_col >= num_cols:
            valid = False

        # Check if the new position is a wall
        if valid:  # Only check for walls if bounds are okay
            if maze[new_row][new_col] == 3 or maze[new_row][new_col] == 5:
                valid = False

        # Return the validity status
        return valid

    # def game_end():
    #     pygame.display.flip()
    #     waiting_for_keypress = True
    #     while waiting_for_keypress:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 pygame.quit()
    #                 sys.exit()
    #             elif event.type == pygame.KEYDOWN:
    #                 waiting_for_keypress = False
    #                 break
# this check will be when object is made as npc's wont interract with items
# def check_item_pickup_NPC():


