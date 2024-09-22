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
        self.initialize_game()
        self.state = "PLAYING"  # Game starts in playing state

     def initialize_game(self):  # set the game to its default settings
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
            self.npcs = [NPC(position=pos) for pos in self.npc_positions[0]]
            self.player = Player(position=self.player_positions[0])
            self.item = item(position=self.item_positions[0])
            self.player = Player(position=self.player_positions[0])
            self.player = Player(position=self.player_positions[0], inventory_size=5) #inventory default size
            game_loc_dir = os.path.dirname(__file__)
            directory_path = os.path.join(game_loc_dir, "mazes")
            self.mazes, self.player_positions, self.item_positions, self.npc_positions = self.load_mazes_from_directory(directory_path)
      

     def load_mazes_from_directory(self, directory_path):
        mazes = []
        player_positions = []
        item_positions = []
        npc_positions = []
        for file_name in os.listdir(directory_path):
            with open(os.path.join(directory_path, file_name), "r") as file:
                maze = []
                player_pos = None
                item_pos = None
                npc_pos = []
                reading_player_position = False
                reading_item_position = False
                reading_npc_positions = False
                for line in file:
                    line = line.strip()
                    if line == "PLAYER_POSITION:":
                        reading_player_position = True
                        reading_item_position = False
                        reading_npc_positions = False
                        continue
                    elif line == "ITEM_POSITION:":
                        reading_player_position = False
                        reading_item_position = True
                        reading_npc_positions = False
                        continue
                    elif line == "NPC_POSITIONS:":
                        reading_player_position = False
                        reading_item_position = False
                        reading_npc_positions = True
                        continue
                    if reading_player_position:
                        player_pos = [int(x) for x in line.split(',')]
                    elif reading_item_position:
                        item_pos = [int(x) for x in line.split(',')]
                    elif reading_npc_positions:
                        npc_pos.append([int(x) for x in line.split(',')])
                    else:
                        maze.append([int(char) for char in line])
                mazes.append(maze)
                player_positions.append(player_pos)
                item_positions.append(item_pos)
                npc_positions.append(npc_pos)
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
     
class Game:
    def __init__(self, maze_file):
        pygame.init()

        # Setup display, clock, etc.
        self.tile_size = 50
        self.screen_width = 1250
        self.screen_height = 1250
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()

        # Load maze, player, NPCs, and items
        self.maze = Maze.load_from_file(maze_file)
        self.player = Player(position=self.maze.player_position)
        self.npcs = [NPC(position=pos) for pos in self.maze.npc_positions]
        self.items_in_game = self.maze.generate_items(Consumable_items)

        # Load assets
        self.load_assets()

    def load_assets(self):
        # Loading images and other assets
        self.images = {
            "background": pygame.image.load("background.png"),
            "item": pygame.image.load("item.png"),
            "player": pygame.image.load("player.png"),
        }

    def main_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Game logic and rendering
            self.screen.blit(self.images["background"], (0, 0))
            self.draw_player()
            self.draw_npcs()
            self.draw_items()

            pygame.display.flip()
            self.clock.tick(30)

#what is an npc
class game_State:
    
    def display_game_over(self):
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over! Press any key to restart.", True, (255, 0, 0))  # Red text
        text_rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        self.screen.blit(self.images["background"], (0, 0))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

    def display_game_win(self):
        font = pygame.font.Font(None, 74)
        text = font.render("You Win! Press any key to restart.", True, (0, 255, 0))  # Green text
        text_rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        self.screen.blit(self.images["background"], (0, 0))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

    def restart_game(self):
        # Reset game state here
        self.initialize_game()  # You may need to refine this to reset all positions, etc.
        self.state = "PLAYING"
class Maze:
    def __init__(self, layout, player_position, npc_positions, item_positions):
        self.layout = layout
        self.player_position = player_position
        self.npc_positions = npc_positions
        self.item_positions = item_positions

    @classmethod
    def load_from_file(cls, file_path):
        with open(file_path, 'r') as f:
            maze_data = json.load(f)

        layout = maze_data["layout"]
        player_position = maze_data["player_position"]
        npc_positions = maze_data["npc_positions"]
        item_positions = maze_data["item_positions"]
        return cls(layout, player_position, npc_positions, item_positions)

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
    def __init__(self, position):
        self.position = position
#how does an npc move
    def move(self, is_move_valid):
        direction = random.choice([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])
        row, col = self.position

        if direction == pygame.K_UP:
            new_row = row - 1
            new_col = col
        elif direction == pygame.K_DOWN:
            new_row = row + 1
            new_col = col
        elif direction == pygame.K_LEFT:
            new_row = row
            new_col = col - 1
        elif direction == pygame.K_RIGHT:
            new_row = row
            new_col = col + 1
        else:
            return  # Skip invalid moves

        if is_move_valid(new_row, new_col):
            self.position[0] = new_row
            self.position[1] = new_col
#what is a player
class Player:
    def __init__(self, position, inventory_size=5):
        self.position = position
        self.inventory = []
        self.inventory_size = inventory_size

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
class item:
    def __init__(self, position):
        self.position = position

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position
#atributes of the item
class item_attributes(item):
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


