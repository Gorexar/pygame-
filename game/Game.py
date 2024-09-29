import os
import pygame
from AssetLoader import AssetLoader
from Player import Player
from NPC import NPC
from Maze import Maze
from consumable_items import Consumable_items  # Import your item list
import random

class Game:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Get base directory
        self.image_dir = os.path.join(base_dir, 'images')
        self.maze_dir = os.path.join(base_dir, 'mazes')

        # Initialize assets and images
        self.asset_loader = AssetLoader(self.image_dir)
        self.asset_loader.load_all()
        self.images = self.asset_loader.images

        # Initialize game elements
        self.tile_size = 50
        self.current_maze_index = 0
        self.mazes = []
        self.current_maze = None
        self.player = Player(self.images["player"], (1, 1), self.tile_size)
        self.npcs = []
        self.items = []
        self.state = "PLAYING"
        self.player_positions = []
        self.npc_positions = []
        self.item_positions = []

    def initialize_game(self):
        self.WIDTH, self.HEIGHT = 1250, 1250
        self.tile_size = 50

        # Load and resize images
        self.resize_images(self.images, self.tile_size, self.WIDTH, self.HEIGHT)
        self.images["background"] = pygame.image.load(os.path.join(self.image_dir, "backgrounds/background_image_light.png"))
        background_width, background_height = self.images["background"].get_size()
        self.screen = pygame.display.set_mode((background_width, background_height))
        self.clock = pygame.time.Clock()

        # Set game window properties
        pygame.display.set_caption("Maze Game for Anastazja!")
        self.icon = self.images["player"]
        self.state = "PLAYING"
        
        # Load the mazes from the maze directory
        self.mazes, self.player_positions, self.item_positions, self.npc_positions = self.load_mazes_from_directory(self.maze_dir)

        if not self.mazes:
            print("No maze loaded.")
            return

        # Initialize the first maze
        self.current_maze_index = 0
        self.current_maze = Maze(
            self.mazes[self.current_maze_index],
            self.player_positions[self.current_maze_index],
            self.npc_positions[self.current_maze_index],
            self.item_positions[self.current_maze_index]
        )

        # Initialize player position
        self.player_position = self.player_positions[self.current_maze_index]
        self.player = Player(self.images["player"], self.player_position, self.tile_size)

        # Initialize NPCs
        self.npcs = [NPC(image=self.images["npc"], position=pos, tile_size=self.tile_size, maze=self.current_maze)
                     for pos in self.npc_positions[self.current_maze_index]]

        # Initialize items
        self.items = self.current_maze.generate_items(Consumable_items)

        print("Game initialized!")

    def load_mazes_from_directory(self, directory_path):
        """
        Load all mazes from a given directory.
        """
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

    def resize_images(self, images, tile_size, width, height):
        """
        Resize all images for the maze, player, NPCs, and items.
        """
        for key in images:
            images[key] = pygame.transform.scale(images[key], (tile_size, tile_size))
        images["background"] = pygame.transform.scale(images["background"], (width, height))

    def initialize_npcs(self):
        # Get a fresh copy of valid positions for NPCs
        npc_valid_positions = self.current_maze.get_valid_positions()

        self.npcs = []

        # Ensure NPC positions are valid
        for npc_position in self.npc_positions[self.current_maze_index]:
            # If position is empty or invalid, assign a random valid position
            if not npc_position or len(npc_position) != 2:
                print(f"Invalid NPC position detected: {npc_position}. Assigning random valid position.")
                if npc_valid_positions:
                    npc_position = random.choice(npc_valid_positions)  # Assign random valid position
                    npc_valid_positions.remove(npc_position)  # Avoid duplicate positions
                else:
                    print("No valid positions left for NPC placement!")
                    continue

            # Ensure position is a tuple (row, col)
            npc_position = tuple(npc_position)

            # Check if position is valid and create NPC
            if self.current_maze.is_valid_position(npc_position):
                npc = NPC(self.images["npc"], npc_position, self.tile_size, maze=self.current_maze)
                self.npcs.append(npc)
            else:
                print(f"Skipping invalid NPC position: {npc_position}")

        print("NPCs initialized with positions:", [npc.position for npc in self.npcs])
    def update_npcs(self):
            for npc in self.npcs:
                npc.move(self.current_maze)  # Move the NPCs


    def handle_input(self):
        """
        Handle player input for movement (WASD or arrow keys).
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.player.move("up", self.current_maze)
        elif keys[pygame.K_DOWN]:
            self.player.move("down", self.current_maze)
        elif keys[pygame.K_LEFT]:
            self.player.move("left", self.current_maze)
        elif keys[pygame.K_RIGHT]:
            self.player.move("right", self.current_maze)

    def draw_player(self):
        """
        Draw the player on the screen.
        """
        self.player.draw(self.screen)

    def draw_npcs(self):
        """
        Draw NPCs on the screen.
        """
        for npc in self.npcs:
            npc.draw(self.screen)

    def draw_items(self):
        """
        Draw all items on the screen.
        """
        for item in self.items.values():  # Assuming self.items is a dictionary
            item.draw(self.screen)

    def draw_maze(self):
        """
        Draw the maze layout on the screen.
        """
        if not hasattr(self, 'current_maze') or self.current_maze is None:
            print("Error: current_maze is not initialized.")
            return

        for row in range(len(self.current_maze.layout)):
            for col in range(len(self.current_maze.layout[row])):
                tile_value = self.current_maze.layout[row][col]
                if tile_value == 1:  # Path
                    self.screen.blit(self.images["path"], (col * self.tile_size, row * self.tile_size))
                elif tile_value in (5, 3):  # Walls or obstacles
                    self.screen.blit(self.images["wall"], (col * self.tile_size, row * self.tile_size))
                elif tile_value == 0:  # Border
                    self.screen.blit(self.images["border"], (col * self.tile_size, row * self.tile_size))

    def render(self):
        """
        Render the game visuals.
        """
        self.screen.blit(self.images["background"], (0, 0))
        self.draw_maze()
        self.draw_player()
        self.draw_npcs()
        self.draw_items()
        pygame.display.flip()
    
    def main_loop(self):
        """
        Main game loop to keep the game running.
        """
        while self.state == "PLAYING":
            # Handle Pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = "QUIT"
                    return  # Exit the loop and quit the game

            # Handle player input and update game state
            self.handle_input()
            self.update_npcs()
            # Render the game visuals
            self.render()

            # Control the frame rate (set to 60 FPS)
            self.clock.tick(60)  # Limit the frame rate to avoid overworking the CPU

        # Quit Pygame cleanly if the loop ends
        pygame.quit()