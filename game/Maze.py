#maze.py
import random
import json

from ConsumableItem import ConsumableItem

class Maze:
    def __init__(self, layout, player_position, npc_positions, item_positions):
        """
        Initialize the Maze object with layout, player, NPC, and item positions.
        
        :param layout: 2D list representing the maze structure.
        :param player_position: Tuple (row, col) representing the player's start position.
        :param npc_positions: List of tuples representing NPC starting positions.
        :param item_positions: List of tuples representing item positions.
        """
        self.layout = layout
        self.player_position = player_position
        self.npc_positions = npc_positions
        self.item_positions = item_positions

    @classmethod
    def load_from_file(cls, file_path):
        """
        Load a maze from a JSON file.
        :param file_path: Path to the maze JSON file.
        :return: A new instance of Maze, or None if there's an error.
        """
        try:
            with open(file_path, 'r') as f:
                maze_data = json.load(f)

            # Ensure required keys are in the JSON data
            required_keys = ["layout", "player_position", "npc_positions", "item_positions"]
            if not all(key in maze_data for key in required_keys):
                raise ValueError("Maze data is missing required keys.")

            layout = maze_data["layout"]
            player_position = maze_data["player_position"]

            # Filter and ensure NPC positions are tuples
            npc_positions = [tuple(pos) if pos else None for pos in maze_data["npc_positions"]]
            # Filter and ensure item positions are tuples
            item_positions = [tuple(pos) if pos else None for pos in maze_data["item_positions"]]

            return cls(layout, player_position, npc_positions, item_positions)

        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            print(f"Error loading maze from {file_path}: {e}")
            return None
            

    def get_valid_positions(self):
        """
        Return a list of valid positions (not walls or obstacles) in the maze.
        
        :return: A list of valid (row, col) positions.
        """
        valid_positions = []
        for row in range(len(self.layout)):
            for col in range(len(self.layout[row])):
                if self.layout[row][col] == 1:  # Only tiles with value 1 are valid
                    valid_positions.append((row, col))
        return valid_positions


    def is_valid_position(self, position):
        # Ensure the position is a valid tuple and not (None, None)
        if position is None or not isinstance(position, tuple) or len(position) != 2 or position == (None, None):
            print(f"Invalid position format or None values: {position}")
            return False
        
        row, col = position
        
        # Ensure the position is within the bounds of the maze
        if not (0 <= row < len(self.layout) and 0 <= col < len(self.layout[0])):
            print(f"Position {position} is out of bounds.")
            return False

        # Check if the tile at the position is walkable (1)
        if self.layout[row][col] == 1:
          
            return True
        else:
            print(f"Position {position} is invalid: Tile value is {self.layout[row][col]}")
            return False




    def generate_items(self, consumable_items_list):
        """
        Generate items in the maze based on predefined positions or randomly if none are available.

        :param consumable_items_list: Dictionary of items to be placed.
        :return: Dictionary of items with their positions set.
        """
        valid_positions = self.get_valid_positions()  # Get all valid positions (tiles with value of 1)

        items = {}
        max_attempts = 100  # Prevent infinite loops in case no valid position is found

        for idx, (item_name, item_data) in enumerate(consumable_items_list.items()):
            # Try to use a predefined position from the maze.json file
            if idx < len(self.item_positions):
                predefined_position = self.item_positions[idx]
            else:
                predefined_position = None  # No predefined position available

            # If predefined position is valid, use it; otherwise, find a random position
            if predefined_position and self.is_valid_position(predefined_position):
                print(f"Using predefined valid position for item {item_name}: {predefined_position}")
                item_data.position = predefined_position
            else:
                print(f"No valid predefined position for item {item_name}. Finding random position...")
                random_position = None
                attempts = 0
                # Loop to find a valid random position
                while not random_position or not self.is_valid_position(random_position):
                    if attempts >= max_attempts:
                        print(f"Failed to find valid position for item {item_name} after {max_attempts} attempts.")
                        break
                    random_position = random.choice(valid_positions)
                    attempts += 1
                print(f"Spawning item at random valid position: {random_position}")
                item_data.position = random_position  # Set the random valid position

            # Add the item with its set position to the dictionary
            items[item_name] = item_data

        return items

    
   
   
    def generate_npcs(self, npcs):
        valid_positions = self.get_valid_positions()  # Get valid walkable positions from the maze

        for idx, npc in enumerate(npcs):
            npc_position = self.npc_positions[idx] if idx < len(self.npc_positions) else None

            # Check if the predefined position is valid
            if npc_position and self.is_valid_position(npc_position):
                print(f"Using predefined valid position for NPC {idx}: {npc_position}")
            else:
                print(f"No valid predefined position for NPC {idx}. Finding random position...")
                npc_position = None
                while not npc_position or not self.is_valid_position(npc_position):
                    npc_position = random.choice(valid_positions)  # Assign a random valid position
                valid_positions.remove(npc_position)  # Avoid duplicate NPCs on the same tile
                print(f"Spawning NPC at random valid position: {npc_position}")

            npc.set_position(npc_position)
            self.rect.topleft = (self.position[1] * self.tile_size, self.position[0] * self.tile_size)
        return npcs
