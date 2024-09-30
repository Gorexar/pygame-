import pygame

class Actions:
    def __init__(self, player, npcs, items, current_maze, tile_size):
        self.player = player
        self.npcs = npcs
        self.items = items
        self.current_maze = current_maze
        self.tile_size = tile_size  # Store tile size for use in environ
    