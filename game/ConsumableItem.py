import os
import pygame  # pygame is used for loading images

from item_attributes import ItemAttributes  # Import ItemAttributes from item_attributes.py

class ConsumableItem(ItemAttributes):  # ConsumableItem inherits from ItemAttributes
    def __init__(self, image, position, tile_size, item_name, item_size, item_type, value=0, description=""):
        if position is None or position == (None, None):
            position = (0, 0)  # Default position
        # Call the parent class constructor (ItemAttributes) and pass all required arguments
        super().__init__(image, position, tile_size, item_type, item_name, value, item_size)
        
        # ConsumableItem-specific attributes
        self.description = description  # Store the description of the item

    def use(self, target):
        """
        Use the consumable item on a target.
        Reduces the item's value after use and applies the effect to the target.
        
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
        Apply the consumable item's effect to the target.
        This method should be overridden with specific effect logic.
        
        :param target: The target to apply the effect to (e.g., a player or NPC).
        """
        pass  # Effect logic should go here (e.g., healing, boosting stats, etc.)

    def __str__(self):
        """
        Return a string representation of the consumable item.
        """
        return f"{self.name} (Type: {self.item_type}, Size: {self.item_size}, Value: {self.value}, Description: {self.description})"
