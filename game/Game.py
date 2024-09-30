#game.py
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

        # Initialize items (always done after loading maze)
        self.items = self.current_maze.generate_items(Consumable_items)

        # Initialize NPCs (after maze and valid positions are set)
        self.initialize_npcs()

        # Initialize actions with player, NPCs, and items after maze has been set
      


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
        """
        Update the NPCs: Move them and handle collision with the player.
        Remove dead NPCs from the game.
        """
        for npc in self.npcs[:]:  # Iterate over a copy to safely remove NPCs
            if npc.is_alive:
                npc.move(self.current_maze)  # Move NPCs that are still alive
                # Check for collisions between player and NPC
                if self.player.rect.colliderect(npc.rect):
                    print(f"Collision detected between player and NPC at {npc.position}")
                    # Apply damage to both player and NPC
                    self.player.take_damage(20)
                    npc.take_damage(20)
                    print(f"After collision: Player health: {self.player.health}, NPC health: {npc.health}")
                    if not npc.is_alive:
                        print(f"NPC at {npc.position} has died and will be removed.")
                        self.npcs.remove(npc)  # Remove dead NPC from list
            else:
                self.npcs.remove(npc)  # Ensure dead NPCs are removed from game
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
    def pause_game(self, message):
        """
        Pause the game and display a game-over message.
        """
        font = pygame.font.SysFont("Arial", 48)
        text_surface = font.render(message, True, (255, 0, 0))  # Red text for Game Over
        text_rect = text_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))

        self.screen.blit(self.images["background"], (0, 0))  # Redraw background
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    paused = False
                    self.state = "QUIT"
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    paused = False
                    self.restart_game()  # Call restart_game to reset everything
    def restart_game(self):
            """
            Restart the game by resetting player, NPCs, items, and maze state.
            """
            self.player.position = self.player_positions[self.current_maze_index]  # Reset player position
            self.player.rect.topleft = (self.player.position[0] * self.tile_size, self.player.position[1] * self.tile_size)
            
            # Reload the NPCs and other game elements
            self.current_maze = Maze(
                self.mazes[self.current_maze_index],
                self.player_positions[self.current_maze_index],
                self.npc_positions[self.current_maze_index],
                self.item_positions[self.current_maze_index]
            )
            self.update_npcs()  # Update NPCs
            self.initialize_npcs()  # Reinitialize NPCs
            self.items = self.current_maze.generate_items(Consumable_items)  # Reinitialize items
            self.state = "PLAYING"  # Set state back to PLAYING

            print("Game restarted!")

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
    def check_player_npc_collisions(self):
        """
        Check if the player collides with any NPCs, and if so, apply damage.
        """
        npc_collision_detected = False
        
        # Only check NPCs that are alive for collisions
        for npc in [npc for npc in self.npcs if npc.is_alive]:
            if self.player.rect.colliderect(npc.rect):
                print(f"Collision detected between player and NPC at {npc.position}")
                npc_collision_detected = True

        if not npc_collision_detected:
            print("No NPC collision detected. Checking for environmental collision...")
            self.check_environment_collisions()
    def check_environment_collisions(self):
        """
        Check if the player is colliding with the environment (e.g., walls, borders).
        """
        # Iterate through the maze layout and check for solid tiles (e.g., walls)
        for row in range(len(self.current_maze.layout)):
            for col in range(len(self.current_maze.layout[row])):
                tile_value = self.current_maze.layout[row][col]
                
                # Assuming 5 represents a wall, adjust based on your maze design
                if tile_value == 5:  # Wall tile value
                    wall_rect = pygame.Rect(col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size)
                    
                    if self.player.rect.colliderect(wall_rect):
                        print(f"Player collided with a wall at position ({row}, {col}).")
                        return  # Player collides with a wall; no further checks needed    
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

                # Check if the player is dead, and pause the game
                if self.player.health <= 0:
                    self.state = "PAUSED"
                    self.pause_game("Game Over! Press Enter to Restart")

                if self.state == "PLAYING":
                    self.handle_input()  # Handle player inputs like movement
                    self.update_npcs()   # Update NPC positions or behavior
                    self.remove_dead_npcs()
                    self.render()        # Render everything on the screen
                    self.check_player_npc_collisions()
                    self.clock.tick(5)

            pygame.quit()
