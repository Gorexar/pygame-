import os
import pygame  # pygame is used for loading images

class GameObject:
    def __init__(self, position):
        """
        Initialize the object with a position.
        
        :param position: The (x, y) position of the object in the game world.
        """
        if not isinstance(position, tuple) or len(position) != 2:
            raise ValueError("Position must be a tuple of two coordinates (x, y).")
        self.position = position

    def get_position(self):
        """
        Get the current position of the object.
        
        :return: The (x, y) position of the object.
        """
        return self.position

    def set_position(self, position):
        """
        Set a new position for the object.
        
        :param position: The new (x, y) position of the object.
        """
        if not isinstance(position, tuple) or len(position) != 2:
            raise ValueError("Position must be a tuple of two coordinates (x, y).")
        self.position = position

    def __str__(self):
        """
        Return a string representation of the object.
        
        :return: String representation showing the object's position.
        """
        return f"GameObject at position {self.position}"
