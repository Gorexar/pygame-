import json
import random
import random
import json

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
        """
        Check if a position is valid within the maze. Only positions with value `1` are valid.
        The maze layout values:
        - 1: valid path
        - 3: wall (invalid)
        - 5: obstacle (invalid)
        """
        # Ensure the position is a valid tuple
        if not isinstance(position, tuple) or len(position) != 2 or position == (None, None):
            print(f"Invalid position format or None values: {position}")
            return False

        row, col = position

        # Check if the position is within the bounds of the maze
        if not (0 <= row < len(self.layout) and 0 <= col < len(self.layout[0])):
            return False

        # Check if the tile at the position is a valid path (1)
        if self.layout[row][col] == 1:
            return True
        else:
            print(f"Position {position} is invalid: Tile value is {self.layout[row][col]}")
            return False


    
    def generate_items(self, items):
        """
        Place items in predefined or random valid locations in the maze.
        :param items: A dictionary of item objects.
        """
        valid_positions = self.get_valid_positions()  # Get valid walkable positions from the maze
        item_positions = []

        for item_name, item in items.items():
            item_position = item.position  # Get the item's position from its attributes

            # Check if the item's position is None or invalid, and assign a random valid position if so
            if item_position is None or not self.is_valid_position(item_position):
                print(f"Invalid item position {item_position}. Assigning random valid position.")
                if valid_positions:
                    item_position = random.choice(valid_positions)  # Assign a random valid position
                    valid_positions.remove(item_position)  # Remove to avoid duplicating positions
                else:
                    print(f"No valid positions left for item '{item_name}'! Skipping item placement.")
                    continue  # Skip this item if no valid positions are available
            else:
                print(f"Placing item '{item_name}' at valid position {item_position}")

            # Ensure the position is a tuple
            if isinstance(item_position, list):
                item_position = tuple(item_position)

            # Set the item position and store it
            item.set_position(item_position)
            item_positions.append(item_position)

            print(f"Item '{item_name}' initialized at {item_position}")

        return items

    
    def generate_npcs(self, npcs):
        """
        Place NPCs in predefined or random valid locations in the maze.
        :param npcs: A list or dictionary of NPC objects.
        """
        valid_positions = self.get_valid_positions()  # Get valid walkable positions from the maze

        for idx, npc in enumerate(npcs):
            npc_position = self.npc_positions[idx] if idx < len(self.npc_positions) else None

            # Check if the position is None or invalid, and assign a random valid position if so
            if not self.is_valid_position(npc_position):
                print(f"Invalid NPC position: {npc_position}. Assigning random valid position.")
                if valid_positions:
                    npc_position = random.choice(valid_positions)  # Assign a random valid position
                    valid_positions.remove(npc_position)  # Remove from valid pool to avoid duplication
                else:
                    print("No valid positions left for NPCs!")
                    continue  # Skip this NPC if no valid positions are available

            # Ensure npc_position is a tuple
            npc_position = tuple(npc_position) if isinstance(npc_position, list) else npc_position

            # Assign the NPC to the valid position
            npc.set_position(npc_position)

        return npcs