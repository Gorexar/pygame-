## still fix game over and win open/close game restart stuff
## DICTIONARY TIME APPARENTLY WOO! OTHERWISE THE GAME LOOPS AND LOOPS AND LOOPS!
## will be required for any kind of not insanity game-menu or defult settings of any kind without
## an insane amount of repeated code time to remap {} must get IN statements IN the brain.
## DICTONARY;  NOPE CLASS TIME need to refactor the game init__(self): and clases



import pygame
import sys
import os
import random

# class Game:
#     def __init__(self):   
#         self.WIDTH, self.HEIGHT = 1250, 1250
#         self.tile_size = 50
#         self.image_dir = "images"
#         self.images = self.initialize_images()
#         self.clock = pygame.time.Clock()
#         self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
#         self.pygame.display.set_caption("Maze Game for Anastazja!") 
#         self.resize_images(images, tile_size, WIDTH, HEIGHT)
    #     self.player_pos = [2,2]
    #     self.item_pos = [2,3]
    #     self.game_win = False
    #     self.game_over = False
    #     self.npc_positions = [
    #     [1, 1],  # NPC 1
    #     [12, 12],  # NPC 2
    #     [7, 7],  # NPC 3
    #     [12, 12],  # NPC 4
    #     [3, 17],  # NPC 5
    #     [12, 12],  # NPC 6
    #     [22, 22],  # NPC 7
    #   ]

pygame.init()

# window size FIXED
WIDTH, HEIGHT = 1250,1250
# size of the game tiles (entities)
tile_size = 50
#load assets (pictures & other)
# Directory for images where the game images are stored
image_dir = "images"

##disctonary for the images
images = {
"path": pygame.image.load(os.path.join(image_dir, 'path_image.png')),
    "wall": pygame.image.load(os.path.join(image_dir, 'grass2.png')),
    "goal": pygame.image.load(os.path.join(image_dir, 'goal.png')),
    "border": pygame.image.load(os.path.join(image_dir, 'locust_tree.png')),
    "player": pygame.image.load(os.path.join(image_dir, 'cat.png')),  # Load player image
    "npc": pygame.image.load(os.path.join(image_dir, 'wolf.png')),  # Load NPC image
    "item": pygame.image.load(os.path.join(image_dir, 'goal.png')),  # Load item image
    "background": pygame.image.load(os.path.join(image_dir, 'background_image_light.png'))
      
  }  # Load background image

 ## resiez the pictures in the dictonary 
images["path"] = pygame.transform.scale(images["path"], (tile_size, tile_size))
images["wall"] = pygame.transform.scale(images["wall"], (tile_size, tile_size))
images["goal"] = pygame.transform.scale(images["goal"], (tile_size, tile_size))
images["border"] = pygame.transform.scale(images["border"], (tile_size, tile_size))
images["player"] = pygame.transform.scale(images["player"], (tile_size, tile_size))
images["npc"] = pygame.transform.scale(images["npc"], (tile_size, tile_size))
images["item"] = pygame.transform.scale(images["item"], (tile_size, tile_size))
images["background"] = pygame.transform.scale(images["background"], (WIDTH, HEIGHT))

def initialize_images():
    return {
        "path": pygame.image.load(os.path.join(image_dir, 'path_image.png')),
        "wall": pygame.image.load(os.path.join(image_dir, 'grass2.png')),
        "goal": pygame.image.load(os.path.join(image_dir, 'goal.png')),
        "border": pygame.image.load(os.path.join(image_dir, 'locust_tree.png')),
        "player": pygame.image.load(os.path.join(image_dir, 'cat.png')),
        "npc": pygame.image.load(os.path.join(image_dir, 'wolf.png')),
        "item": pygame.image.load(os.path.join(image_dir, 'goal.png')),
        "background": pygame.image.load(os.path.join(image_dir, 'background_image_light.png'))
    }
def resize_images(images, tile_size, width, height):
    images["path"] = pygame.transform.scale(images["path"], (tile_size, tile_size))
    images["wall"] = pygame.transform.scale(images["wall"], (tile_size, tile_size))
    images["goal"] = pygame.transform.scale(images["goal"], (tile_size, tile_size))
    images["border"] = pygame.transform.scale(images["border"], (tile_size, tile_size))
    images["player"] = pygame.transform.scale(images["player"], (tile_size, tile_size))
    images["npc"] = pygame.transform.scale(images["npc"], (tile_size, tile_size))
    images["item"] = pygame.transform.scale(images["item"], (tile_size, tile_size))
    images["background"] = pygame.transform.scale(images["background"], (width, height))

# Set up clock for FPS control
clock = pygame.time.Clock()

 # create the game 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game for Anastazja!")

# Maze data (grid of 0s and 1s where 0 is path, 3 border, 2 etc HAS TO BE 25x25 PYTHON THINKS THINGS STARTING AT ZERO IS NORMAL
maze = [#MAZE WALL OF ANNOYING
  [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
  [3, 1, 5, 1, 1, 1, 5, 1, 5, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 5, 1, 1, 1, 5, 3],
  [3, 1, 5, 1, 5, 1, 5, 1, 1, 1, 5, 5, 1, 1, 1, 5, 5, 5, 1, 5, 1, 5, 1, 1, 3],
  [3, 1, 5, 1, 5, 1, 5, 1, 5, 5, 1, 1, 5, 5, 5, 1, 1, 5, 1, 5, 1, 5, 5, 1, 3],
  [3, 1, 1, 1, 5, 1, 5, 1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 5, 1, 5, 1, 5, 1, 1, 3],
  [3, 5, 5, 5, 5, 1, 5, 1, 5, 1, 5, 5, 5, 5, 5, 5, 1, 5, 1, 1, 1, 5, 1, 5, 3],
  [3, 1, 1, 1, 1, 1, 5, 1, 5, 1, 1, 1, 1, 1, 1, 5, 1, 5, 5, 5, 5, 5, 1, 1, 3],
  [3, 1, 5, 5, 5, 5, 5, 1, 5, 5, 5, 5, 5, 5, 1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 3],
  [3, 1, 1, 1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 3],
  [3, 5, 5, 5, 5, 5, 5, 5, 5, 1, 5, 1, 5, 5, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
  [3, 1, 5, 5, 1, 1, 1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 5, 5, 5, 5, 5, 5, 5, 1, 3],
  [3, 1, 1, 1, 1, 1, 5, 5, 5, 5, 5, 1, 1, 5, 5, 5, 1, 1, 1, 1, 1, 1, 1, 1, 3],
  [3, 1, 5, 5, 5, 5, 5, 1, 5, 1, 1, 1, 5, 1, 1, 1, 1, 5, 1, 1, 5, 5, 5, 5, 3],
  [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 5, 1, 1, 1, 5, 5, 1, 5, 1, 5, 1, 1, 1, 3],
  [3, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 1, 1, 5, 5, 1, 5, 1, 1, 5, 5, 1, 5, 1, 3],
  [3, 1, 1, 1, 5, 1, 5, 5, 1, 1, 1, 5, 5, 1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 3],
  [3, 1, 5, 1, 5, 1, 1, 1, 1, 5, 5, 1, 1, 1, 5, 5, 1, 1, 5, 1, 1, 1, 5, 1, 3],
  [3, 1, 5, 1, 1, 5, 5, 1, 5, 1, 1, 1, 5, 5, 1, 1, 1, 5, 1, 1, 5, 5, 5, 1, 3],
  [3, 1, 1, 5, 1, 1, 5, 1, 1, 1, 5, 5, 5, 1, 1, 5, 5, 1, 1, 5, 1, 5, 1, 1, 3],
  [3, 5, 1, 1, 5, 1, 5, 5, 5, 5, 1, 1, 1, 1, 5, 5, 1, 1, 5, 1, 1, 1, 1, 5, 3],
  [3, 1, 5, 1, 5, 1, 1, 1, 5, 1, 1, 1, 5, 5, 1, 1, 1, 5, 1, 1, 5, 5, 5, 1, 3],
  [3, 1, 1, 1, 5, 5, 5, 1, 1, 1, 5, 5, 1, 1, 1, 1, 5, 5, 1, 5, 1, 1, 1, 1, 3],
  [3, 1, 5, 5, 1, 1, 1, 5, 5, 5, 1, 1, 1, 5, 5, 5, 5, 1, 1, 5, 1, 5, 1, 5, 3],
  [3, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 5, 5, 1, 1, 1, 1, 1, 1, 1, 1, 5, 1, 1, 3],
  [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
  
]



def initialize_game():
    global player_pos, item_pos, game_win, game_over, npc_positions, images, tile_size, WIDTH, HEIGHT
    images = initialize_images()  # Reset the images dictionary to its original values
    tile_size = 50
    WIDTH, HEIGHT = 1250, 1250  # Example dimensions
    resize_images(images, tile_size, WIDTH, HEIGHT)
    player_pos = [2,2]
    item_pos = [2,3]
    game_win = False
    game_over = False
    npc_positions = [
    [1, 1],  # NPC 1
    [12, 12],  # NPC 2
    [7, 7],  # NPC 3
    [12, 12],  # NPC 4
    [3, 17],  # NPC 5
    [12, 12],  # NPC 6
    [22, 22],  # NPC 7
]
 #random for later   #item_pos = [random.randint(1, 24), random.randint(1, 24)]  # Example item position

    
     

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

def move_npc(npc_positions):
    for npc_pos in npc_positions:
        direction = random.choice([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])
        row, col = npc_pos

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
            continue  # Skip invalid moves

        if is_move_valid(new_row, new_col):
            npc_pos[0] = new_row
            npc_pos[1] = new_col

        new_col = col + 1

def move_player(direction):
    # Get current position
    row, col = player_pos
    
    # Calculate new position based on direction
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
        return

    # Check if the move is valid
    if is_move_valid(new_row, new_col):
        # Update player position if the move is valid
        player_pos[0] = new_row
        player_pos[1] = new_col
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
                
            
                
                
            
            

#if the bunny is touched
def check_item_pickup_Player():
 
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


def main():
    initialize_game()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                move_player(event.key)

        
        # Move NPCs
        move_npc(npc_positions)
        
        # Check for item pickup
        check_item_pickup_Player()
        check_item_pickup_NPC()
        
        # Draw everything
        screen.blit(images["background"], (0, 0))  # Use the background image from the dictionary
        draw_maze()
        draw_player()
        draw_npc()
        draw_item()
        
        # Check for game over or win
        if game_over:
            display_game_over()
            game_end()
        elif game_win:
            display_game_win()
            game_end()
        
        pygame.display.flip()
        clock.tick(3)  # Control the frame rate

# Main game loop
if __name__ == "__main__":
    main()
    

