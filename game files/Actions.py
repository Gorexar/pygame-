class Actions:

    def __init__(self, player, item):
        self.player = player
        self.item = item

    def player_pickup_item(self):
        if self.player.position == self.item.position:
            if not self.player.is_inventory_full():
                self.player.add_to_inventory(self.item)  # Add item to player's inventory
                self.item.position = None  # Remove item from the game
                print("You picked up the item!")
            else:
                print("Inventory full")

    def is_move_valid(self, new_row, new_col, maze):
        num_rows = len(maze)
        num_cols = len(maze[0])
        valid = True

        # Check if the new row is outside play space
        if new_row < 0 or new_row >= num_rows:
            valid = False

        # Check if the new column is out of play space
        if new_col < 0 or new_col >= num_cols:
            valid = False

        # Check if the new position is a wall
        if valid:  # Only check for walls if bounds are okay
            if maze[new_row][new_col] == 3 or maze[new_row][new_col] == 5:
                valid = False

        # Return the validity status
        return valid
