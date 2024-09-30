import pygame
from Maze import Maze
class Actions:
    def __init__(self, player, npcs, items, current_maze, tile_size):
        self.player = player
        self.npcs = npcs
        self.items = items
        self.current_maze = current_maze
        self.tile_size = tile_size  # Store tile size for use in environ
    

    def check_player_npc_collisions(self):
        """
        Check if the player collides with any NPCs.
        Remove NPCs that have died from the list of active NPCs.
        """
        npc_collision_detected = False
        
        # Create a list of NPCs to remove after collision checks
        npcs_to_remove = []
        
        for npc in self.npcs:
            # Ensure the NPC is alive and check for collision
            if npc.is_alive and self.player.rect.colliderect(npc.rect):
                print(f"Collision detected between player and NPC at {npc.position}")
                
                # Mark collision as detected
                npc_collision_detected = True
                
                # If the NPC is dead after the collision, queue it for removal
                if not npc.is_alive:
                    npcs_to_remove.append(npc)
                    print(f"NPC at {npc.position} has died and will be removed.")
        
        # Remove dead NPCs
        for npc in npcs_to_remove:
            self.npcs.remove(npc)  # Remove dead NPCs from the list
        
        if not npc_collision_detected:
            print("No NPC collision detected. Checking for environmental collision...")
            self.check_environment_collisions()
    def check_environment_collisions(self):
        """
        Check if the player is colliding with the environment (e.g., walls, borders).
        """
        # Iterate through the maze layout and check for solid tiles (e.g., walls)
        for row in range(len(self.current_maze.layout)):
            for col in range(len(self.current_maze.layout[row])):
                tile_value = self.current_maze.layout[row][col]
                
                # Assuming 5 represents a wall, adjust based on your maze design
                if tile_value == 5:  # Wall tile value
                    wall_rect = pygame.Rect(col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size)
                    
                    if self.player.rect.colliderect(wall_rect):
                        print(f"Player collided with a wall at position ({row}, {col}).")
                        return  # Player collides with a wall; no further checks needed
        
        # If no wall collision detected
        print("No environment collision detected.")
