import random
maze = [
  [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
  [3, 1, 5, 1, 1, 1, 5, 1, 5, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 5, 1, 1, 1, 5, 3],
  [3, 1, 5, 1, 5, 1, 5, 1, 1, 1, 5, 5, 1, 1, 1, 5, 5, 5, 1, 5, 1, 5, 1, 1, 3],
  [3, 1, 5, 1, 5, 1, 5, 1, 5, 5, 1, 1, 5, 5, 5, 1, 1, 5, 1, 5, 1, 5, 5, 1, 3],
  [3, 1, 1, 1, 5, 1, 5, 1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 5, 1, 5, 1, 5, 1, 1, 3],
  [3, 5, 5, 5, 5, 1, 5, 1, 5, 1, 5, 5, 5, 5, 5, 5, 1, 5, 1, 1, 1, 5, 1, 5, 3],
  [3, 1, 1, 1, 1, 1, 5, 1, 5, 1, 1, 1, 1, 1, 1, 5, 1, 5, 5, 5, 5, 5, 1, 1, 3],
  [3, 1, 5, 5, 5, 5, 5, 1, 5, 5, 5, 5, 5, 5, 1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 3],
  [3, 1, 1, 1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 3],
  [3, 5, 5, 5, 5, 5, 5, 5, 5, 1, 5, 1, 5, 5, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
  [3, 1, 5, 5, 1, 1, 1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 5, 5, 5, 5, 5, 5, 5, 1, 3],
  [3, 1, 1, 1, 1, 1, 5, 5, 5, 5, 5, 1, 1, 5, 5, 5, 1, 1, 1, 1, 1, 1, 1, 1, 3],
  [3, 1, 5, 5, 5, 5, 5, 1, 5, 1, 1, 1, 5, 1, 1, 1, 1, 5, 1, 1, 5, 5, 5, 5, 3],
  [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 5, 1, 1, 1, 5, 5, 1, 5, 1, 5, 1, 1, 1, 3],
  [3, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 1, 1, 5, 5, 1, 5, 1, 1, 5, 5, 1, 5, 1, 3],
  [3, 1, 1, 1, 5, 1, 5, 5, 1, 1, 1, 5, 5, 1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 3],
  [3, 1, 5, 1, 5, 1, 1, 1, 1, 5, 5, 1, 1, 1, 5, 5, 1, 1, 5, 1, 1, 1, 5, 1, 3],
  [3, 1, 5, 1, 1, 5, 5, 1, 5, 1, 1, 1, 5, 5, 1, 1, 1, 5, 1, 1, 5, 5, 5, 1, 3],
  [3, 1, 1, 5, 1, 1, 5, 1, 1, 1, 5, 5, 5, 1, 1, 5, 5, 1, 1, 5, 1, 5, 1, 1, 3],
  [3, 5, 1, 1, 5, 1, 5, 5, 5, 5, 1, 1, 1, 1, 5, 5, 1, 1, 5, 1, 1, 1, 1, 5, 3],
  [3, 1, 5, 1, 5, 1, 1, 1, 5, 1, 1, 1, 5, 5, 1, 1, 1, 5, 1, 1, 5, 5, 5, 1, 3],
  [3, 1, 1, 1, 5, 5, 5, 1, 1, 1, 5, 5, 1, 1, 1, 1, 5, 5, 1, 5, 1, 1, 1, 1, 3],
  [3, 1, 5, 5, 1, 1, 1, 5, 5, 5, 1, 1, 1, 5, 5, 5, 5, 1, 1, 5, 1, 5, 1, 5, 3],
  [3, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 5, 5, 1, 1, 1, 1, 1, 1, 1, 1, 5, 1, 1, 3],
  [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
  
]
def get_random_position(value):
    """Get a random position for a given value in the maze."""
    valid_positions = [(x, y) for x in range(25) for y in range(25) if maze[x][y] == value]
    return random.choice(valid_positions) if valid_positions else None

# Randomize player position
PLAYER_POSITIONS = get_random_position(1)

# Randomize NPC positions
NPC_POSITIONS = [get_random_position(1) for _ in range(4)]

# Randomize item positions
ITEM_POSITIONS = [
    {'name': 'food', 'position': get_random_position(1)},
    {'name': 'tiny scratching post', 'position': get_random_position(1)},
    {'name': 'water bowl', 'position': get_random_position(1)},
    {'name': 'catnip toy', 'position': get_random_position(1)},
    {'name': 'treats', 'position': get_random_position(1)},
    {'name': 'feather wand', 'position': get_random_position(1)},
    {'name': 'laser pointer', 'position': get_random_position(1)},
    {'name': 'cat bed', 'position': get_random_position(1)},
    {'name': 'litter box', 'position': get_random_position(1)},
    {'name': 'scratching pad', 'position': get_random_position(1)},
]

# Print positions to verify
print("Player Position:", PLAYER_POSITIONS)
print("NPC Positions:", NPC_POSITIONS)
print("Item Positions:", [item['position'] for item in ITEM_POSITIONS])