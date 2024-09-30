#game.py
import os
import pygame
from AssetLoader import AssetLoader
from Player import Player
from NPC import NPC
from Maze import Maze
from consumable_items import Consumable_items  # Import your item list
import random
from Actions    import Actions
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

        # Initialize items (always done after loading maze)
        self.items = self.current_maze.generate_items(Consumable_items)

        # Initialize NPCs (after maze and valid positions are set)
        self.initialize_npcs()

        # Initialize actions with player, NPCs, and items after maze has been set
        print(f"Current Maze: {self.current_maze}")
        self.actions = Actions(self.player, self.npcs, self.items, self.current_maze, self.tile_size)


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
        valid_positions = self.current_maze.get_valid_positions()  # Get valid walkable positions from the maze
        self.npcs = []

        for idx, npc_position in enumerate(self.npc_positions[self.current_maze_index]):
            # Check if the position is None or invalid, and assign a random valid position if so
            if npc_position is None or not self.current_maze.is_valid_position(npc_position):
                print(f"Invalid NPC position: {npc_position}. Assigning random valid position.")
                if valid_positions:
                    npc_position = random.choice(valid_positions)  # Assign a random valid position
                    valid_positions.remove(npc_position)  # Remove from valid pool to avoid duplication
                else:
                    print("No valid positions left for NPCs! Skipping NPC initialization.")
                    continue  # Skip this NPC if no valid positions are available
            else:
                print(f"Spawning NPC at valid position: {npc_position}")

            # Ensure position is a tuple
            if isinstance(npc_position, list):
                npc_position = tuple(npc_position)

            # Initialize the NPC at the valid position
            npc = NPC(self.images["npc"], npc_position, self.tile_size, maze=self.current_maze)
            self.npcs.append(npc)

        print("NPCs initialized with positions:", [npc.position for npc in self.npcs])

        
    def update_npcs(self):
        for npc in self.npcs:
            npc.move(self.current_maze)  # Move each NPC
            # Check for collisions with the player
            if self.player.rect.colliderect(npc.rect):
                print(f"Collision detected between player and NPC at {npc.position}")
                # Apply damage to both
                self.player.take_damage(20)
                npc.take_damage(20)
                print(f"After collision: Player health: {self.player.health}, NPC health: {npc.health}")

        

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            print("Player moving up")  # Add debug to confirm input
            self.player.move("up", self.current_maze)
        elif keys[pygame.K_DOWN]:
            print("Player moving down")  # Add debug to confirm input
            self.player.move("down", self.current_maze)
        elif keys[pygame.K_LEFT]:
            print("Player moving left")  # Add debug to confirm input
            self.player.move("left", self.current_maze)
        elif keys[pygame.K_RIGHT]:
            print("Player moving right")  # Add debug to confirm input
            self.player.move("right", self.current_maze)
    def check_player_npc_collisions(self):
        """
        Check if the player collides with any NPCs, and if so, apply damage.
        """
        for npc in self.npcs:
            if self.player.rect.colliderect(npc.rect):  # Check collision
                print(f"Collision detected between player and NPC at {npc.position}")
                self.player.take_damage(10)  # Apply damage to the player
                npc.take_damage(10)  # Apply damage to the NPC

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
            # Only draw NPCs that are alive and have a valid position and rect
            if npc.is_alive and npc.rect is not None:
                npc.draw(self.screen)
                pygame.draw.rect(self.screen, (0, 255, 0), npc.rect, 2)  # Green rectangles for alive NPCs
            else:
                print(f"Skipping NPC at {npc.position} because it is dead or has an invalid position.")

    def remove_dead_npcs(self):
        """
        Remove all NPCs that are dead from the game.
        """
        self.npcs = [npc for npc in self.npcs if npc.is_alive]  # Only keep alive NPCs

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
        pygame.draw.rect(self.screen, (255, 0, 0), self.player.rect, 2)  # Red rectangle for the player
        for npc in self.npcs:
            pygame.draw.rect(self.screen, (0, 255, 0), npc.rect, 2)  # Green rectangles for the NPCs

            pygame.display.flip()  # Update the screen
    def main_loop(self):
        while self.state == "PLAYING":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = "QUIT"
                    return
            print(f"Player Position: {self.player.position}, Player Rect: {self.player.rect}")
            for idx, npc in enumerate(self.npcs):
                print(f"NPC {idx} Position: {npc.position}, NPC Rect: {npc.rect}")
            
            # This is the correct place to check collisions after all movements
        

            self.handle_input()    # Handle player inputs like movement
            self.update_npcs()     # Update NPC positions or behavior
            self.remove_dead_npcs()
            self.render()          # Render everything on the screen
            self.actions.check_player_npc_collisions()
            print(f"Collision detected at: {npc.position}. Player health: {self.player.health}, NPC health: {npc.health}")

            self.clock.tick(5)

        pygame.quit()
