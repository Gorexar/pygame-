# To do list
# #1 complete transition to multiple game files.
# #2 refactor the way movement and item interaction is going to be handled. orignal scope was too narrow.
# 3# flush out the scope of the game and settle on a features and final game design.

class Game:
    def __init__(self):
        self.asset_loader = AssetLoader("images")
        self.asset_loader.load_all()
        self.images = self.asset_loader.images
        self.tile_size = 50  # Set your desired tile size (in pixels)
        self.current_maze_index = 0  # Start with the first maze
        self.mazes = []  # Initialize mazes as an empty list
        self.current_maze = None
        self.player = Player(self.images["player"], (1, 1), self.tile_size)
        self.npcs = [NPC(self.images["npc"], (3, 4), self.tile_size), NPC(self.images["npc"], (5, 6), self.tile_size)]
        self.state = "PLAYING"  # Set initial state
        self.player_positions = []  # Initialize player_positions
        self.npc_positions = []  # Initialize npc_positions

    def initialize_game(self):
        self.WIDTH, self.HEIGHT = 1250, 1250
        self.tile_size = 50
        self.image_dir = "images"
        self.images = self.initialize_images()  # Ensure this method is defined
        self.resize_images(self.images, self.tile_size, self.WIDTH, self.HEIGHT)
        self.images["background"] = pygame.image.load(os.path.join(self.image_dir, "backgrounds/background_image_light.png"))
        background_width, background_height = self.images["background"].get_size()  # Override the background image size for now
        self.screen = pygame.display.set_mode((background_width, background_height))
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Maze Game for Anastazja!")
        self.icon = self.images["player"]
        self.game_over = False
        self.game_win = False
        self.state = "PLAYING"
        print("Initializing game...")
        print("NPC positions:", self.npc_positions)
        print("Maze:", self.current_maze)

        directory_path = "mazes"  # Adjust this to your directory
        self.mazes, self.player_positions, self.item_positions, self.npc_positions = self.load_mazes_from_directory(directory_path)

        if not self.mazes:
            print("No maze loaded.")
            return  # Exit initialization if no mazes are available

        self.current_maze_index = 0  # Start with the first maze
        self.current_maze = Maze(
            self.mazes[self.current_maze_index],
            self.player_positions[self.current_maze_index],
            self.npc_positions[self.current_maze_index],
            self.item_positions[self.current_maze_index]
        )

        self.player_position = self.player_positions[self.current_maze_index]
        self.player = Player(self.images["player"], self.player_position, self.tile_size)

        self.npcs = [NPC(image=self.images["npc"], position=pos, tile_size=self.tile_size, maze=self.current_maze) for pos in self.npc_positions[self.current_maze_index]]

        print("Game initialized!")
        print("NPC positions:", self.npc_positions[self.current_maze_index])
        print("Maze:", self.current_maze)
        print("Player position:", self.player_position)
        print("Item positions:", self.item_positions[self.current_maze_index])

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

    def draw_items(self):
        for item in self.current_maze.items:
            item.draw(self.screen)

    def initialize_images(self):
        print(os.path.join(self.image_dir, "sprites/player.png"))
        print(os.path.join(self.image_dir, "sprites/npc.png"))
        print(os.path.join(self.image_dir, "sprites/path.png"))
        print(os.path.join(self.image_dir, "sprites/wall.png"))
        print(os.path.join(self.image_dir, "sprites/Scraching_post_item.png"))
        images = {
            "player": pygame.image.load(os.path.join(self.image_dir, "sprites/player.png")),
            "npc": pygame.image.load(os.path.join(self.image_dir, "sprites/npc.png")),
            "path": pygame.image.load(os.path.join(self.image_dir, "sprites/path.png")),
            "wall": pygame.image.load(os.path.join(self.image_dir, "sprites/wall.png")),
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
                elif tile_value == 5 or tile_value == 3:
                    self.screen.blit(self.images["wall"], (col * self.tile_size, row * self.tile_size))
                elif tile_value == 0:  # Wall
                    self.screen.blit(self.images["border"], (col * self.tile_size, row * self.tile_size))
                # Add more conditions for other elements if needed

    def get_random_position(self, value):
        print(type(self.current_maze))  # Should be <class '__main__.Maze'>
        valid_positions = [(x, y) for x in range(len(self.current_maze.layout))
                           for y in range(len(self.current_maze.layout[0]))
                           if self.current_maze.layout[x][y] == value]
        return random.choice(valid_positions) if valid_positions else None

    def reset_player_and_npcs(self):
        self.player_positions = self.get_random_position(1)  # Update the player position
        self.npc_positions = [self.get_random_position(1) for _ in range(4)]  # Update NPC positions
        self.player.position = self.player_positions

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
            npc.move(self.current_maze)
            npc.draw(self.screen)

    def load_maze(self, file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)  # Return the maze data as a dictionary
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return None
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file: {file_path}")
            return None

    def handle_game_states(self):
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

                if action.is_move_valid(new_row, new_col, self.current_maze.layout):
                    self.player.move(direction, self.current_maze)  # Update player position if valid

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
                    if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                        direction = None
                        if event.key == pygame.K_UP:
                            direction = "up"
                        elif event.key == pygame.K_DOWN:
                            direction = "down"
                        elif event.key == pygame.K_LEFT:
                            direction = "left"
                        elif event.key == pygame.K_RIGHT:
                            direction = "right"

                        if direction:
                            self.player.move(direction, self.current_maze)

                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                    else:
                        print(f"Key {pygame.key.name(event.key)} was pressed, but no action is defined yet.")

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

    def render(self):
        self.screen.blit(self.images["background"], (0, 0))
        self.draw_maze()  # Draw the maze
        self.draw_player()
        self.draw_npcs()
        self.draw_items()
        pygame.display.flip()