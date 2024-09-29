
class Actions:
    def __init__(self, player, npcs=None, items=None):
        """
        Initialize the Actions class with a player, optional NPCs, and list of items.
        
        :param player: The player object.
        :param npcs: A list of NPC objects (optional).
        :param items: A list of item objects in the game (optional).
        """
        self.player = player
        self.npcs = npcs if npcs else []  # List of NPCs
        self.items = items if items else []  # List of items in the game
        
    def player_pickup_item(self):
        """
        Handle the logic for the player picking up an item.
        """
        for item in self.items:
            if self.player.position == item.position:
                if not self.player.is_inventory_full():
                    self.player.add_to_inventory(item)  # Add item to player's inventory
                    item.position = None  # Remove the item from the game
                    print(f"You picked up {item.item_name}!")
                else:
                    print(f"Inventory full! You have {len(self.player.inventory)}/{self.player.inventory_size} items.")
                return
        print("No item to pick up here.")

    def interact_with_npc(self, npc):
        """
        Handle interaction between the player and an NPC.
        """
        if self.player.position == npc.position:
            print(f"You are interacting with {npc.name}.")
            # Add your game-specific interaction logic here
            # Example: Start conversation, start battle, trade, etc.
        else:
            print(f"{npc.name} is not nearby to interact with.")

    def use_item(self, user, item, target=None):
        """
        Handle the logic for using an item (by player or NPC) on a target.
        
        :param user: The player using the item.
        :param item: The item being used.
        :param target: The target of the item (optional, could be an NPC or player).
        """
        if item in user.inventory:
            print(f"{user.name} is using {item.item_name}.")
            item.use(target)  # This assumes the item has a 'use' method for effects
            if item.item_value <= 0:  # Assuming 'item_value' reduces as the item is used
                user.inventory.remove(item)  # Remove item when fully used
                print(f"{item.item_name} has been used up and removed from {user.name}'s inventory.")
        else:
            print(f"{user.name} doesn't have {item.item_name} in their inventory.")

    def is_move_valid(self, new_row, new_col, maze):

        num_rows = len(maze)
        num_cols = len(maze[0])

        # Check if the new position is outside the maze bounds
        if new_row < 0 or new_row >= num_rows or new_col < 0 or new_col >= num_cols:
            print(f"Move to ({new_row}, {new_col}) is out of bounds.")
            return False

        # Check if the new position is a wall or obstacle
        if maze[new_row][new_col] in (3, 5):  # Assuming 3 and 5 represent walls or obstacles
            print(f"Move to ({new_row}, {new_col}) is blocked by a wall or obstacle.")
            return False

        return True  # If both checks pass, the move is valid
