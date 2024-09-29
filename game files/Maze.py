class Maze: #the maze and how it functions (maze layout and maze data player locations item npc are all loaded in seprtate.json 
    # init self layout player position npc positions item positions <-- turns these into veribles i can define later
    def __init__(self, layout, player_position, npc_positions, item_positions):
        self.layout = layout
        self.player_position = player_position
        self.npc_positions = npc_positions
        self.item_positions = item_positions
        self.tile_size = 50  # Set your desired tile size (in pixels)
    @classmethod #idk yet has to do with the json demon file
    def load_from_file(cls, file_path):
        try:
            with open(file_path, 'r') as f:
                maze_data = json.load(f)
            
            # what keys are required in the json file (the maze file)
            required_keys = ["layout", "player_position", "npc_positions", "item_positions"]
            if not all(key in maze_data for key in required_keys):
                raise ValueError("Maze data is missing required keys.")
            # if the keys are met then it will create definitions of layout player position npc positions and item positions<-- as veribles set by the map file
            layout = maze_data["layout"] #in map file
            player_position = maze_data["player_position"] #in map file
            npc_positions = maze_data["npc_positions"] #in map file
            item_positions = maze_data["item_positions"] #in map file
            #will add here for objects.
            return cls(layout, player_position, npc_positions, item_positions)
        
        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            print(f"Error loading maze from {file_path}: {e}")
            return None  
        #error if the maze dosent load
        
    def get_valid_positions(self): #defining the valid positions in the maze 
        """Return a list of valid positions (not walls or obstacles)"""
        valid_positions = [] #valid_positions [] empty list that is going to ask what locations are in the list 
        for row in range(len(self.layout)):#complicated string to read the layout of the maze
            for col in range(len(self.layout[row])):#complicated string to read the layout of the maze
                if self.layout[row][col] not in (3, 5):  # Exclude walls and obstacles
                    valid_positions.append([row, col])
        return valid_positions
    
    def is_valid_position(self, position):
       #Check if a position is valid within the maze#
        row, col = position
        # Check if the position is within bounds and is not a wall
        return (0 <= row < len(self.layout) and 
                0 <= col < len(self.layout[0]) and 
                self.layout[row][col] == 1)  # Assuming 1 represents a valid path
    # definding how to "spawn" items in the game, askes if there is a set location in the maze file. 
    # otherwise it will ask what positions are considered vaid, and spawn them in random positions.
    def generate_items(self, items):
        print("Generating items...")
        """Place items in predefined or random valid locations."""
        valid_positions = self.get_valid_positions()
        
        for item in items.values():  # Iterate directly over the item objects
            if item.get_item_position() is None:  # Check if the item has no position
                random_pos = random.choice(valid_positions)
                valid_positions.remove(random_pos) # removes each item's location from the valid positions list give by the mazelayout
                item.set_position(random_pos)  # Set the item's position
        
        return items
    print("Finished generating items.")
