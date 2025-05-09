from backend.oram_core.recursive_oram import RecursivePathORAM

oram = RecursivePathORAM(n_blocks=256)

for i in range(200):
    oram.write(i, f"value-{i}")
    if i % 25 == 0:
        stats = oram.dump_stats()
        print(f"Batch {i} — Stash size: {stats['main_oram']['stash_size']}, Non-empty buckets: {stats['main_oram']['non_empty_buckets']}")
