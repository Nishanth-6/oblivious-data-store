from backend.oram_core.recursive_oram import RecursivePathORAM

def test_write_and_read_back():
    oram = RecursivePathORAM(n_blocks=16)
    oram.write(7, "testing")
    value = oram.read(7)
    assert value == "testing", "Read should return the same value written"

def test_position_remap():
    oram = RecursivePathORAM(n_blocks=16)
    oram.write(3, "alpha")
    leaf1 = oram.pos_map_oram.read(3)
    _ = oram.read(3)
    leaf2 = oram.pos_map_oram.read(3)
    assert leaf1 != leaf2, "Position should remap to a new leaf after access"

def test_access_log_non_empty():
    oram = RecursivePathORAM(n_blocks=8)
    oram.write(1, "x")
    oram.read(1)
    logs = oram.get_access_log()
    assert len(logs) >= 2, "Access log should record each operation"

def test_stats_structure():
    oram = RecursivePathORAM(n_blocks=8)
    stats = oram.dump_stats()
    assert "main_oram" in stats and "pos_map_oram" in stats, "Stats should include both ORAM layers"
    assert "stash_size" in stats["main_oram"], "Main ORAM stats missing fields"
