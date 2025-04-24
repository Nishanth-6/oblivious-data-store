"""
Very small, purely in-memory Path-ORAM implementation.
• Tree height L = ceil(log2(N)) − 1      (for N leaves)
• Bucket size Z = 4                       (good empirical choice)
This is NOT production-ready – just enough to demonstrate the algorithm.
"""

import math
import os
import random
from collections import defaultdict
from typing import List, Dict, Any

class PathORAM:
    def __init__(self, n_blocks: int, bucket_size: int = 4):
        self.N = n_blocks                       # logical blocks (0 .. N-1)
        self.Z = bucket_size
        self.L = math.ceil(math.log2(self.N)) - 1
        self.num_buckets = 2 ** (self.L + 1) - 1
        # Each bucket: list of up-to-Z data entries or None
        self.tree: Dict[int, List[Any]] = defaultdict(list)
        # Position map: logical->leaf index
        self.pos_map = {i: self._rand_leaf() for i in range(self.N)}
        # Simple stash
        self.stash: Dict[int, Any] = {}
        self.access_log: List[int] = []

    # ---------- public API ----------
    def read(self, idx: int):
        return self._access(idx, op="read", new_val=None)

    def write(self, idx: int, val):
        return self._access(idx, op="write", new_val=val)

    # ---------- core algorithm ----------
    def _access(self, idx: int, op: str, new_val):
        leaf = self.pos_map[idx]
        self.access_log.append(leaf)
        self.pos_map[idx] = self._rand_leaf()        # remap before returning

        # 1. Fetch path from root to leaf into stash
        path = self._path_nodes(leaf)
        for bucket in path:
            self.stash_update_from_bucket(bucket)

        # 2. If write, update stash copy
        if op == "write":
            self.stash[idx] = new_val
        result = self.stash.get(idx)                # could be None for read-miss

        # 3. Evict from stash back into path (leaf->root so deeper nodes fill first)
        for bucket in reversed(path):
            while len(self.tree[bucket]) < self.Z:
                # choose a stash block whose mapped leaf is under this bucket
                candidate = self._find_stash_block(bucket)
                if candidate is None:
                    break
                self.tree[bucket].append((candidate, self.stash.pop(candidate)))

        return result

    # ---------- helpers ----------
    def _path_nodes(self, leaf: int):
        """Return bucket IDs from root (0) down to given leaf."""
        node = (2 ** self.L - 1) + leaf             # index of leaf bucket
        path = []
        while node >= 0:
            path.append(node)
            if node == 0:
                break
            node = (node - 1) // 2
        return path

    def _rand_leaf(self):
        return random.randint(0, 2 ** self.L - 1)

    def stash_update_from_bucket(self, bucket_id: int):
        # move everything from bucket into stash, then empty bucket
        for logical, data in self.tree[bucket_id]:
            self.stash[logical] = data
        self.tree[bucket_id].clear()

    def _find_stash_block(self, bucket_id: int):
        """Return a logical block whose mapped leaf is in this subtree."""
        subtree_leaves = self._subtree_leaf_range(bucket_id)
        for logical in list(self.stash):            # iterate copy
            if self.pos_map[logical] in subtree_leaves:
                return logical
        return None

    def _subtree_leaf_range(self, bucket_id: int):
        """Return the set(range) of leaves under a given bucket."""
        # convert bucket_id back to (level, offset)
        level = int(math.log2(bucket_id + 1))
        first_leaf = (bucket_id + 1) - 2 ** level
        span = 2 ** (self.L - level)
        return range(first_leaf * span, (first_leaf + 1) * span)

    # ---------- debug ----------
    def dump_stats(self):
        return {
            "stash_size": len(self.stash),
            "non_empty_buckets": sum(bool(self.tree[b]) for b in self.tree)
        }
        
    def get_access_log(self):
        return self.access_log
