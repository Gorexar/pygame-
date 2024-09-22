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

class Game_Defaults:
     DEFAULT_SETTINGS = {
        "tile_size": 50,
        "WIDTH": 1250,
        "HEIGHT": 1250,
        "player_pos": [2, 2],
        "item_pos": [2, 3],
        "game_win": False,
        "game_over": False,
        "npc_positions": [
            [1, 1],  # NPC 1
            [12, 12],  # NPC 2
            [7, 7],  # NPC 3
            [12, 12],  # NPC 4
            [3, 17],  # NPC 5
            [12, 12],  # NPC 6
            [22, 22],  # NPC 7
        ],
    }
     
     def __init__(self):
        self.initialize_game()

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
            self.player_pos = [2,2]
            self.item_pos = [2,3]
            self.game_win = False
            self.game_over = False
            self.npc_positions = [
         [1, 1],  # NPC 1
         [12, 12],  # NPC 2
         [7, 7],  # NPC 3
         [12, 12],  # NPC 4
         [3, 17],  # NPC 5
         [12, 12],  # NPC 6
         [22, 22],  # NPC 7
       ]
         
         ## had to read up on how to use OS to read files in the installed location, not my personal PC HD LOC
         #this looks for where the game (this file) is located. then looks for the mazes folder and loads the maze
         # this will allow me to add more mazes later and have them load in the game
            game_loc_dir = os.path.dirname(__file__)
            directory_path = os.path.join(game_loc_dir, "mazes")
            self.mazes = self.load_mazes_from_directory(directory_path)

     #this is taking the maze file ive created and loading it into the game as a maze its using a list of lists
     def load_mazes_from_directory(self, directory_path):
            mazes = []
            for file_name in os.listdir(directory_path):
                with open(os.path.join(directory_path, file_name), "r") as file:
                    maze = []
                    for line in file:
                        maze.append([int(char) for char in line.strip()])
                    mazes.append(maze)
            return mazes
     
     
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
     
     def main(self):
        self.initialize_game()
        while True:
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                self.move_player(event.key)

        
        # Move NPCs
            self.move_npc(self.npc_positions)
        
        # Check for item pickup
            self.check_item_pickup_Player()
            self.check_item_pickup_NPC()
            
            # Draw everything
            self.screen.blit(self.images["background"], (0, 0))  # Use the background image from the dictionary
            self.draw_player()
            self.draw_npc()
            self.draw_item()
            
            # Check for game over or win
            if self.game_over:
                self.display_game_over()
                self.game_end()
            elif self.game_win:
                self.display_game_win()
                self.game_end()
            
            pygame.display.flip()
            self.clock.tick(3)  # Control the frame rate

class NPC:
    def __init__(self, position):
        self.position = position

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

class Player:
    def __init__(self, position): #what is self......
        self.position = position
        #where is self....
    def get_position(self):
        return self.position
        #you know where self is, but lets get it again
    def set_position(self, position):
        self.position = position
        #now that self is self, and self knows where self is. let see if self can move self.
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
# for making an item i need to define what paramters im using for the item in the self (self): part

# if not careful i could spider web out classes and types and function hierarchies ad nauseum
class Item:
    def __init__(self, item_type, item_name, item_position): #item_value#
        self.item_type = item_type
        self.item_name = item_name
        self.item_position = item_position
        #self.item_value = item_value
        #item is an item, and it has a type, a name, and a position. 
            
#
#
#class rules:
   # def is_move_valid(new_row, new_col):
    #    num_rows = 25
    #    num_cols = 25
    #    valid = True

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
#class Conditions:
    def game_end():
        pygame.display.flip()
        waiting_for_keypress = True
        while waiting_for_keypress:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    waiting_for_keypress = False
                    break
def player_pickpup_item():
    item
 



    global item_pos, game_win
    if player_pos == item_pos:

        if random.randint(1, 1) == 1: #10% of the time you win and game
            game_win = True
        else:
            while True: #90% of the time it teleports
                new_row = random.randint(1, 23)
                new_col = random.randint(1, 23)
                if is_move_valid(new_row, new_col):
                    item_pos[0] = new_row
                    item_pos[1] = new_col
                    print("The bunny escaped through a hole!")
                    break

def check_item_pickup_NPC():
    global item_pos, game_over

    for npc_pos in npc_positions:
        if npc_pos == item_pos:
            if random.randint(1, 10) == 1:  # 10% chance to win
                print("The monster got the bunny!")
                game_over = True
                break  # Trigger game over
            else:  # 90% chance to teleport the item
                while True:
                    new_row = random.randint(0, 24)
                    new_col = random.randint(0, 24)
                    if is_move_valid(new_row, new_col):
                        item_pos[0] = new_row
                        item_pos[1] = new_col
                        print("The bunny escaped a monster!")
                        break

def display_game_over():
    font = pygame.font.Font(None, 74)
    global images
    images["npc"] = pygame.transform.scale(images["npc"], (WIDTH, HEIGHT))
    text = font.render("The wolves ate the bunny! Press any key to restart!", True, (255, 0, 0))  # Red color text
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(images["npc"], (0, 0))
    screen.blit(text, text_rect)
    pygame.display.flip()
waiting_for_keypress = True




def display_game_win():
    font = pygame.font.Font(None, 74)
    global images
    images["npc"] = pygame.transform.scale(images["npc"], (WIDTH, HEIGHT))
    text = font.render("You caught the bunny!! Press any key to restart!", True, (0, 255, 0))  # Green color text
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(images["player"], (0, 0))
    screen.blit(text, text_rect)
waiting_for_keypress = True


 #*****DRAWING THE GAME******


def draw_player():
    screen.blit(images["player"], (player_pos[1] * tile_size, player_pos[0] * tile_size))
    #npc
def draw_npc():
    for npc_pos in npc_positions:
        screen.blit(images["npc"], (npc_pos[1] * tile_size, npc_pos[0] * tile_size))

#item
def draw_item():
    screen.blit(images["item"], (item_pos[1] * tile_size, item_pos[0] * tile_size))



#how do we create the maze reads the number of colums  the number of rows (#25) is used as a border with #00
def draw_maze():
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            x = col * tile_size
            y = row * tile_size
            if maze[row][col] == 1:
                screen.blit(images["path"], (x, y))
            elif maze[row][col] == 5:
                screen.blit(images["wall"], (x, y))
            elif maze[row][col] == 3:
                screen.blit(images["border"], (x, y))
            elif maze[row][col] == 2:
                screen.blit(images["goal"], (x, y))


