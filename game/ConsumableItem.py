# ConsumableItem.py
import pygame
from item_attributes import ItemAttributes

class ConsumableItem(ItemAttributes):
    def __init__(self, image, tile_size, item_name, item_size, item_type, value=0, description=""):
        """
        Initialize a consumable item.
        
        :param image: Image for the item.
        :param tile_size: Size of the tile in the grid.
        :param item_name: Name of the item.
        :param item_size: Size of the item.
        :param item_type: Type of the item (e.g., food, object).
        :param value: Item's value or usage count.
        :param description: Description of the item.
        """
        # Provide a temporary valid position (0, 0) to avoid errors in the Item class
        super().__init__(image, (0, 0), tile_size, item_type, item_name, value, item_size)

        # Item-specific attributes
        self.description = description
        self.position = None  # Position will be set later by the maze

    def draw(self, screen):
        """
        Draw the item on the screen at its current position.
        
        :param screen: The screen surface to draw the item on.
        """
        if self.position:
            x, y = self.position[1] * self.tile_size, self.position[0] * self.tile_size  # Adjust based on tile size
            screen.blit(self.image, (x, y))  # Draw the image at the calculated position

    def use(self, target):
        """
        Use the item on a target.
        
        :param target: The player or NPC on which the item is used.
        """
        if self.value > 0:
            self.apply_effect(target)
            self.value -= 1
            print(f"{self.name} used on {target}. {self.value} remaining. {self.description}")
        else:
            print(f"No {self.name} left to use. {self.description}")

    def apply_effect(self, target):
        """
        Apply the item's effect to the target.
        
        This should be overridden by specific item effect logic.
        """
        pass  # This should be overridden in specific item types.

    def __str__(self):
        """
        String representation of the item.
        """
        return f"{self.name} (Type: {self.item_type}, Size: {self.item_size}, Value: {self.value}, Description: {self.description})"
