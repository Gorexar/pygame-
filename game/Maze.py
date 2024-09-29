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
            npc_positions = maze_data["npc_positions"]
            item_positions = maze_data["item_positions"]
            
            return cls(layout, player_position, npc_positions, item_positions)

        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            print(f"Error loading maze from {file_path}: {e}")
            return None


    def get_valid_positions(self):
        """
        Return a list of valid positions (not walls or obstacles) in the maze.
        Returns a new copy each time to avoid conflicts between NPCs and items.
        """
        valid_positions = []
        for row in range(len(self.layout)):
            for col in range(len(self.layout[row])):
                if self.layout[row][col] == 1:  # Assuming 1 is a valid path.
                    valid_positions.append((row, col))
        return valid_positions.copy()  # Return a copy of the list


    def is_valid_position(self, position):
        """
        Check if a position is valid within the maze.
        
        :param position: Tuple (row, col) representing the position to check.
        :return: True if the position is valid, False otherwise.
        """
        if not isinstance(position, tuple) or len(position) != 2:
            raise ValueError("Position must be a tuple of (row, col).")
        
        row, col = position
        return (
            0 <= row < len(self.layout) and 
            0 <= col < len(self.layout[0]) and 
            self.layout[row][col] == 1  # Assuming 1 represents a valid path.
        )

    def generate_items(self, items):
        # Get a fresh copy of valid positions for items
        item_valid_positions = self.get_valid_positions()

        for idx, item in enumerate(items.values()):
            # Assign a random valid position for each item
            if idx < len(self.item_positions):
                item_position = self.item_positions[idx]
            else:
                if item_valid_positions:
                    item_position = random.choice(item_valid_positions)
                    item_valid_positions.remove(item_position)  # Avoid duplicate positions
                else:
                    print("No valid positions left for item placement!")
                    continue

            if isinstance(item_position, list):
                item_position = tuple(item_position)

            # Assign position and ensure it's valid
            if self.is_valid_position(item_position):
                item.set_position(item_position)
            else:
                print(f"Skipping invalid item position: {item_position}")

        return items
