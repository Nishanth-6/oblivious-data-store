import json
import os

def serialize_oram(oram):
    return {
        "tree": {k: v for k, v in oram.tree.items()},
        "stash": oram.stash,
        "pos_map": oram.pos_map
    }

def deserialize_oram(oram, data):
    oram.tree.update({int(k): v for k, v in data["tree"].items()})
    oram.stash.update({int(k): v for k, v in data["stash"].items()})
    oram.pos_map.update({int(k): v for k, v in data["pos_map"].items()})

def save_recursive_oram(roram, path="recursive_oram_state.json"):
    data = {
        "main_oram": serialize_oram(roram.main_oram),
        "pos_map_oram": serialize_oram(roram.pos_map_oram)
    }
    with open(path, "w") as f:
        json.dump(data, f)
    return True

def load_recursive_oram(roram, path="recursive_oram_state.json"):
    if not os.path.exists(path):
        return False
    with open(path, "r") as f:
        data = json.load(f)
    deserialize_oram(roram.main_oram, data["main_oram"])
    deserialize_oram(roram.pos_map_oram, data["pos_map_oram"])
    return True
