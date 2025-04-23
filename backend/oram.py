import random

class SimpleORAM:
    def __init__(self, size=16):
        self.size = size
        self.storage = {i: None for i in range(size)}
        self.access_log = []
        self.position_map = {i: i for i in range(size)}

    def read(self, index):
        physical = self.position_map[index]
        self.access_log.append(physical)
        return self.storage.get(physical)

    def write(self, index, value):
        # 1) Pick a new random physical slot
        new_physical = random.randint(0, self.size - 1)
        # 2) Update the map so that future reads go here
        self.position_map[index] = new_physical
        # 3) Log the access
        self.access_log.append(new_physical)
        # 4) Store the value at that slot
        self.storage[new_physical] = value

    def get_access_log(self):
        return self.access_log
