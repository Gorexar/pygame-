from .Item import Item  # Ensure the Item class is in the same directory or adjust the import path accordingly

class ItemAttributes(Item):
    def __init__(self, image, position, tile_size, item_type, item_name, item_value, item_size):
        """
        Initialize the item with additional attributes.
        
        :param image: The image representing the item.
        :param position: The (x, y) position of the item in the maze.
        :param tile_size: The size of each tile in the maze.
        :param item_type: The type of the item (e.g., weapon, food, etc.).
        :param item_name: The name of the item.
        :param item_value: The value of the item (e.g., healing amount, damage, etc.).
        :param item_size: The size of the item in the inventory.
        """
        super().__init__(image, position, tile_size)
        self.item_type = item_type
        self.item_name = item_name
        self.item_value = item_value
        self.item_size = item_size

    def __str__(self):
        """
        Return a string representation of the item attributes.
        
        :return: A string describing the item.
        """
        return (
            f"Item: {self.item_name}\n"
            f"Type: {self.item_type}\n"
            f"Size: {self.item_size}\n"
            f"Value: {self.item_value}\n"
            f"Position: {self.get_position()}"
        )

    def get_item_position(self):
        """
        Get the current position of the item.
        
        :return: The (x, y) position of the item.
        """
        return self.get_position()
