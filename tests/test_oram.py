from backend.oram_core.path_oram import PathORAM

def test_basic_read_write():
    oram = PathORAM(n_blocks=8)
    oram.write(3, "A")
    assert oram.read(3) == "A"
    oram.write(3, "B")
    assert oram.read(3) == "B"
