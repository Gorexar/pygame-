#Items implimented
#all game files split up 
# next fix is npcs and items failure to spawn/crash game with no value given random generation of items and npcs broken?



import os
import pygame
from AssetLoader import AssetLoader
from Maze import Maze
from Item import Item
from item_attributes import ItemAttributes
from ConsumableItem import ConsumableItem
from Player import Player
from NPC import NPC
from Actions import Actions
from Game import Game
from consumable_items import Consumable_items



def main():
    """
    Main function to initialize and start the game.
    This function performs the following steps:
    1. Determines the base directory where the script is located.
    2. Creates paths for the 'mazes' and 'images' directories relative to the base directory.
    3. Prints the list of files in the 'mazes' directory.
    4. Loads a maze from a JSON file located in the 'mazes' directory.
    5. If the maze is loaded successfully, it prints the player, NPC, and item positions.
    6. Initializes the Pygame library.
    7. Creates and initializes a Game object.
    8. Starts the main game loop.
    If the maze fails to load, it prints an error message.
    """
    # Get the directory where this script is located
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Create paths relative to the base directory
    maze_dir = os.path.join(base_dir, 'mazes')
    image_dir = os.path.join(base_dir, 'images')

    # Print files in the maze directory
    print("Files in mazes directory:", os.listdir(maze_dir))

    # Load the maze
    maze_file = os.path.join(maze_dir, 'maze_1.json')
    maze = Maze.load_from_file(maze_file)
    
    if maze:
        print("Maze loaded successfully.")
        print(f"Player Position: {maze.player_position}")
        print(f"NPC Positions: {maze.npc_positions}")
        print(f"Item Positions: {maze.item_positions}")

        # Initialize the game
        pygame.init()

        # Create a Game object (assuming Game class is structured accordingly)
        game = Game()  # Game initialization updated here
        game.initialize_game()

        # Start the game loop
        game.main_loop()
    else:
        print("Failed to load maze.")

if __name__ == "__main__":
    main()
