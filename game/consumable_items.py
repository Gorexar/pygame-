# consumable_items.py
import os
import pygame  # pygame is used for loading images
from ConsumableItem import ConsumableItem  # Import the ConsumableItem class

# Load item images
food_image = pygame.image.load(os.path.join("images", "sprites", "food.png"))
tiny_scratching_post_image = pygame.image.load(os.path.join("images", "sprites", "scratching_post.png"))
treat_image = pygame.image.load(os.path.join("images", "sprites", "treat.png"))
medical_treat_image = pygame.image.load(os.path.join("images", "sprites", "medical_treat.png"))
catnip_image = pygame.image.load(os.path.join("images", "sprites", "catnip.png"))

tile_size = 50  # Define the size of each tile

# Define consumable items without positions; positions will be set by the maze later
Consumable_items = {
    "food": ConsumableItem(
        image=food_image,
        tile_size=tile_size,
        item_name="food",
        item_size=1,
        item_type="food",
        value=10,
        description="Heals 10 HP"
    ),
    "tiny_scratching_post": ConsumableItem(
        image=tiny_scratching_post_image,
        tile_size=tile_size,
        item_name="tiny scratching post",
        item_size=1,
        item_type="object",
        value=10,
        description="Sharpens claws"
    ),
    "treats": ConsumableItem(
        image=treat_image,
        tile_size=tile_size,
        item_name="treats",
        item_size=1,
        item_type="treat",
        value=50,
        description="Heals 50 HP"
    ),
    "medical_treats": ConsumableItem(
        image=medical_treat_image,
        tile_size=tile_size,
        item_name="medical treats",
        item_size=1,
        item_type="treat",
        value=10,
        description="Cures poison & bleeding"
    ),
    "catnip": ConsumableItem(
        image=catnip_image,
        tile_size=tile_size,
        item_name="catnip",
        item_size=1,
        item_type="treat",
        value=20,
        description="Makes you feel good +20 HP +5 speed"
    ),
}
