import os
import random
import json
import pygame

# Import classes from their respective files
from AssetLoader import AssetLoader
from Maze import Maze
from Item import Item
from objects import objects
from item_attributes import item_attributes
from ConsumableItem import ConsumableItem
from Player import Player
from NPC import NPC
from Actions import Actions
from Game import Game
from consumable_items import Consumeable_items  # Import the consumable items

print("Files in mazes directory:", os.listdir(r"C:\Users\gorex\Desktop\pygame!\game files"))

if __name__ == "__main__":
    maze = Maze.load_from_file("mazes/maze_1.json")
    if maze:
        print("Maze loaded successfully.")
        print("Player Position:", maze.player_position)
        print("NPC Positions:", maze.npc_positions)
        print("Item Positions:", maze.item_positions)
        pygame.init()
        game = Game()  # Create an instance of your game
        game.initialize_game()
        game.main_loop()  # Start the game loop