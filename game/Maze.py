import json
import random
import pygame  # pygame is used for loading images

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
        self.tile_size = 50  # Set your desired tile size (in pixels)

    @classmethod
    def load_from_file(cls, file_path):

        try:
            with open(file_path, 'r') as f:
                maze_data = json.load(f)
            
            required_keys = ["layout", "player_position", "npc_positions", "item_positions"]
            if not all(key in maze_data for key in required_keys):
                raise ValueError("Maze data is missing required keys.")
            
            layout = maze_data["layout"]
            player_position = tuple(maze_data["player_position"])
            npc_positions = [tuple(pos) for pos in maze_data["npc_positions"]]
            item_positions = [tuple(pos) for pos in maze_data["item_positions"]]
            
            return cls(layout, player_position, npc_positions, item_positions)

        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            print(f"Error loading maze from {file_path}: {e}")
            return None  # Optionally re-raise or return None depending on use case.

    def get_valid_positions(self):
        """
        Return a list of valid positions (not walls or obstacles) in the maze.
        
        :return: A list of valid (row, col) positions.
        """
        valid_positions = []
        for row in range(len(self.layout)):
            for col in range(len(self.layout[row])):
                if self.layout[row][col] == 1:  # Assuming 1 is a valid path.
                    valid_positions.append((row, col))
        return valid_positions

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
        """
        Place items in predefined or random valid locations.
        
        :param items: Dictionary of item objects to be placed in the maze.
        """
        print("Generating items...")
        valid_positions = self.get_valid_positions()

        for item in items.values():
            if item.get_position() is None:  # If the item doesn't have a set position
                if not valid_positions:  # Check if there are valid positions left
                    raise ValueError("No valid positions left to place items.")
                
                random_pos = random.choice(valid_positions)
                valid_positions.remove(random_pos)  # Remove the chosen position from the list
                item.set_position(random_pos)  # Set the item's position
        
        print("Finished generating items.")
        return items
