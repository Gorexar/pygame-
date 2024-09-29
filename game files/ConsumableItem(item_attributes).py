from item_attributes import item_attributes

class ConsumableItem(item_attributes):
    def __init__(self, name, item_size, item_type, value=0):
        super().__init__()
        self.name = name
        self.item_size = item_size
        self.item_type = item_type
        self.value = value

    def use(self, target):
        if self.value > 0:
            self.apply_effect(target)
            self.value -= 1
            print(f"{self.name} used on {target}. {self.value} remaining.")
        else:
            print(f"No {self.name} left to use.")

    def apply_effect(self, target):
        # Logic to apply the effect to the target
        pass

    def __str__(self):
        return f"{self.name} (Type: {self.item_type}, Size: {self.item_size}, Value: {self.value})"