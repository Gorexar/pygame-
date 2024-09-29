from .ConsumableItem import ConsumableItem

Consumeable_items = {
    "food": ConsumableItem(
        name="food",
        ###description="Heals 10 HP",
        item_size=1,
        item_type="food",
        value=10
    ),
    "tiny scratching post": ConsumableItem(
        name="tiny scratching post",
        ###description="Sharpens claws a small amount",
        item_size=1,
        item_type="object"
    ),
    "tasty treats": ConsumableItem(
        name="Treats",
        ###description="tasty treats Heals 50 HP",
        item_size=1,
        item_type="treat",
        value=50
    ),
    "medical treats": ConsumableItem(
        name="medical treats",
        ###description="Cures poison & bleeding",
        item_size=1,
        item_type="treat"
    ),
    "catnip": ConsumableItem(
        name="catnip",
        ###description="Makes you feel good +20 HP +5 speed",
        item_size=1,
        item_type="treat",
        value=20
    ),
}