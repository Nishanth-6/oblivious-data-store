from backend.oram_core.path_oram import PathORAM
import random

class RecursivePathORAM:
    def __init__(self, n_blocks: int, bucket_size: int = 4):
        self.N = n_blocks
        self.Z = bucket_size
        self.main_oram = PathORAM(n_blocks=n_blocks, bucket_size=bucket_size)

        # ORAM1 stores position map of main_oram (one block per entry)
        self.pos_map_oram = PathORAM(n_blocks=n_blocks, bucket_size=bucket_size)

        # Init: assign each logical block in ORAM0 a random leaf in ORAM Tree
        for i in range(n_blocks):
            initial_leaf = random.randint(0, 2**(self.main_oram.L) - 1)
            self.pos_map_oram.write(i, initial_leaf)

    def read(self, idx: int):
        leaf = self.pos_map_oram.read(idx)
        result = self.main_oram._access(idx, op="read", new_val=None, override_leaf=leaf)
        new_leaf = random.randint(0, 2**(self.main_oram.L) - 1)
        self.pos_map_oram.write(idx, new_leaf)
        return result

    def write(self, idx: int, value):
        leaf = self.pos_map_oram.read(idx)
        self.main_oram._access(idx, op="write", new_val=value, override_leaf=leaf)
        new_leaf = random.randint(0, 2**(self.main_oram.L) - 1)
        self.pos_map_oram.write(idx, new_leaf)

    def get_access_log(self):
        return self.main_oram.get_access_log()

    def dump_stats(self):
        return {
            "main_oram": self.main_oram.dump_stats(),
            "pos_map_oram": self.pos_map_oram.dump_stats()
        }
