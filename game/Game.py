import os
import pygame
import random
from AssetLoader import AssetLoader
from Player import Player
from NPC import NPC
from Actions import Actions
from Maze import Maze


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
        self.npcs = [NPC(self.images["npc"], (3, 4), self.tile_size), NPC(self.images["npc"], (5, 6), self.tile_size)]
        self.state = "PLAYING"
        self.player_positions = []
        self.npc_positions = []

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

        # Set player and NPC positions
        self.player_position = self.player_positions[self.current_maze_index]
        self.player = Player(self.images["player"], self.player_position, self.tile_size)
        self.npcs = [NPC(image=self.images["npc"], position=pos, tile_size=self.tile_size, maze=self.current_maze)
                     for pos in self.npc_positions[self.current_maze_index]]
        
        
        self.initialize_npcs()
        print("Game initialized!")

    def initialize_npcs(self):
        """
        Initialize NPCs at random locations if their positions are not provided.
        """
        valid_positions = self.current_maze.get_valid_positions()  # Get valid positions in the maze

        # Create NPCs, assigning random valid positions if needed
        self.npcs = []
        for npc_position in self.npc_positions[self.current_maze_index]:
            if not npc_position:  # If position is blank or None
                npc_position = random.choice(valid_positions)
                valid_positions.remove(npc_position)  # Remove this position to avoid duplicates

            npc = NPC(image=self.images["npc"], position=npc_position, tile_size=self.tile_size, maze=self.current_maze)
            self.npcs.append(npc)
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
        for key in images:
            images[key] = pygame.transform.scale(images[key], (tile_size, tile_size))
    def update_npcs(self):
        for npc in self.npcs:
            npc.move(self.current_maze)  # Make sure the NPCs move based on the maze layout


    def handle_input(self):
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
        self.player.draw(self.screen)

    def draw_npcs(self):
        for npc in self.npcs:
            npc.draw(self.screen)

    def draw_maze(self): # this is where i can change tile values to change the maze or add more objects as strucures like path/wall/border
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

        self.screen.blit(self.images["background"], (0, 0))
        self.draw_maze()
        self.draw_player()
        self.draw_npcs()
        pygame.display.flip()
        for npc in self.npcs:
                npc.draw(self.screen)

    def main_loop(self):
        """
        The main game loop that keeps the game running until the player quits.
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Handle input, update game state, and render everything
            self.handle_input()
            self.render()
            self.update_npcs()
            
            
            # Control frame rate (psudo game speed for now)
            self.clock.tick(5)

        pygame.quit()  # Quit Pygame when the game loop exits
