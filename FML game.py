## still fix game over and win open/close game restart stuff



import pygame
import sys
import os
import random


# Initialize Pygame
pygame.init()

# window size FIXED
WIDTH, HEIGHT = 1250,1250
# size of the game tiles (entities)
tile_size = 50
#load assets (pictures & other)
# Directory for images where the game images are stored
image_dir = "images"
# Load images
path_image = pygame.image.load(os.path.join(image_dir, 'path_image.png'))
wall_image = pygame.image.load(os.path.join(image_dir, 'grass2.png'))
goal_image = pygame.image.load(os.path.join(image_dir, 'goal.png'))
border_image = pygame.image.load(os.path.join(image_dir, 'locust_tree.png'))
player_image = pygame.image.load(os.path.join(image_dir, 'cat.png'))  # Load player image
npc_image = pygame.image.load(os.path.join(image_dir, 'wolf.png'))  # Load NPC image
item_image = pygame.image.load(os.path.join(image_dir, 'goal.png'))  # Load item image
background_image = pygame.image.load(os.path.join(image_dir, 'background_image_light.png'))  # Load background image
# resize the images in-program (too lazy to edit source image)
path_image = pygame.transform.scale(path_image, (50, 50))
wall_image = pygame.transform.scale(wall_image, (50, 50))
goal_image = pygame.transform.scale(goal_image, (50, 50))
border_image = pygame.transform.scale(border_image, (50, 50))
player_image = pygame.transform.scale(player_image, (50, 50))
npc_image = pygame.transform.scale(npc_image, (50, 50))
item_image = pygame.transform.scale(item_image, (50, 50))
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

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

#DEFAULT Entity spawn locations#
player_pos = [2,2]
npc_positions = [
    [1, 1],  # NPC 1
    [12, 12],  # NPC 2
    [7, 7],  # NPC 3
    [12, 12],  # NPC 4
    [3, 17],  # NPC 5
    [12, 12],  # NPC 6
    [22, 22],  # NPC 7
]
game_win = False
game_over = False
item_pos = [2,3]
        #allows the player to move X entity in this case the player one) i think?

def initialize_game():
    global player_pos, item_pos, game_win, game_over
    player_pos = [1, 1]  # Example starting position
    item_pos = [random.randint(1, 24), random.randint(1, 24)]  # Example item position
    game_win = False
    game_over = False
     

def is_move_valid(new_row, new_col):
    # lazy maze size
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
    


def check_item_pickup():
    
    global item_pos, game_win

    if player_pos == item_pos:
        
        if random.randint(1, 10) == 1: #10% of the time you win and game
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

def display_game_over():
    # Set a game over font and size
    font = pygame.font.Font(None, 74)
    global npc_image
    npc_image = pygame.transform.scale(npc_image, (WIDTH, HEIGHT))
    text = font.render("Game Over! Press any key to restart!", True, (255, 0, 0))  # Red color text
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(npc_image, (0, 0))
    screen.blit(text, text_rect)
    pygame.display.flip()

    # Wait for key press to restart
    waiting_for_keypress = True
    while waiting_for_keypress:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting_for_keypress = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(npc_image, (0, 0))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000) 

    


def display_game_win():
    font = pygame.font.Font(None, 74)
    global player_image
    player_image = pygame.transform.scale(player_image, (WIDTH, HEIGHT))
    text = font.render("You caught the bunny!! Press any key to restart!", True, (0, 255, 0))  # Green color text
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(player_image, (0, 0))
    screen.blit(text, text_rect)

    waiting_for_keypress = True
    while waiting_for_keypress:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting_for_keypress = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(player_image, (0, 0))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)



                
    


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
                


 #*****DRAWING THE GAME******


def draw_player():
    screen.blit(player_image, (player_pos[1] * tile_size, player_pos[0] * tile_size))
    #npc
def draw_npc():
    for npc_pos in npc_positions:
        screen.blit(npc_image, (npc_pos[1] * tile_size, npc_pos[0] * tile_size))

#item
def draw_item():
    screen.blit(item_image, (item_pos[1] * tile_size, item_pos[0] * tile_size))



#how do we create the maze reads the number of colums  the number of rows (#25) is used as a border with #00
def draw_maze():
    num_cols = 25
    num_rows = 25

# Draw the maze
    for row in range(num_rows):
        for col in range(num_cols):
            x = (col) * tile_size #tile_size is just prettier than saying 50)
            y = (row) * tile_size
            if maze[row][col] == 1:
                screen.blit(path_image, (x, y))
            elif maze[row][col] == 2:  # draw walls
                screen.blit(goal_image, (x, y))
            elif maze[row][col] == 3:  # Draw the goal tile
                screen.blit(border_image, (x, y))
            else:
                screen.blit(wall_image, (x, y))

def main():
    main()

def main():
    initialize_game()

# Main game loop
running = True
while running:
    if game_win:
        display_game_win()
        running = False

    if game_over:
        display_game_over()
        running = False


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move_player(pygame.K_UP)
            elif event.key == pygame.K_DOWN:
                move_player(pygame.K_DOWN)
            elif event.key == pygame.K_LEFT:
                move_player(pygame.K_LEFT)
            elif event.key == pygame.K_RIGHT:
                move_player(pygame.K_RIGHT)

    move_npc(npc_positions)
    check_item_pickup_NPC()
    check_item_pickup()



    # Draw the maze and entities
    screen.blit(background_image, (0, 0))
    draw_maze()
    draw_npc()  # Draw all NPCs
    draw_player()
    draw_item()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate aka game speed?
    clock.tick(10)
initialize_game()
