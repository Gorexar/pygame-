import os
import pygame  # pygame is used for loading images

from Item import Item  # Ensure that you are importing Item from the correct file

class ItemAttributes(Item):
    def __init__(self, image, position, tile_size, item_type, item_name, item_value, item_size):
        super().__init__(image, position, tile_size)
        self.item_type = item_type
        self.item_name = item_name
        self.item_value = item_value
        self.item_size = item_size

    def __str__(self):
        return (
            f"Item: {self.item_name}\n"
            f"Type: {self.item_type}\n"
            f"Size: {self.item_size}\n"
            f"Value: {self.item_value}\n"
            f"Position: {self.get_position()}"
        )
