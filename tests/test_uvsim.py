'''
Test file for functionality of UVSim class in uvsim.py
'''
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from uvsim import UVSim
from accumulator import Accumulator

# Test UVSim initialization
def test_default_values():
    sim = UVSim()
    assert sim.ui == None
    assert sim.log == []
    assert sim.memSpace == 0
    assert sim.counter == 0
    assert sim.memory == {i:"0000" for i in range(100)}
    assert isinstance(sim.accum, Accumulator)
    assert sim.record

# Test (40..) branch function
def test_branch():
    sim = UVSim()
    sim.branch(10)
    assert sim.counter == 10
    assert sim.log[-1] == "+4010 : Program branch to 10"

# Test (41..) branchneg function
def test_branchneg():
    sim = UVSim()
    
    sim.branchneg(10)   # test branch fail condition
    assert sim.counter == 0
    assert sim.record is True

    sim.accum.currVal = -1  # test successful branch condition
    sim.branchneg(10)
    assert sim.counter == 10
    assert sim.log[-1] == "+4110 : Program branch to 10"

# Test (42..) branchzero function
def test_branchzero():
    sim = UVSim()

    sim.branchzero(10)  # test successful branch condition
    assert sim.counter == 10
    assert sim.log[-1] == "+4210 : Program branch to 10"

    sim.accum.currVal = 1   # test branch fail condition
    sim.branchzero(20)
    assert sim.counter == 10

# Test inspectCurrent function
def test_inspectCurrent():
    sim = UVSim()
    assert sim.inspectCurrent() == "Program's current state:\nAccumulator: 0\nAction: No instructions loaded"

    sim.accum.currVal = 10
    sim.memSpace = 100
    sim.branch(10)
    assert sim.counter == 10
    assert sim.inspectCurrent() == "Program's current state:\nAccumulator: 10\nAction: +4010 : Program branch to 10"

def test_saveMemory(tmp_path):
    # Setup
    sim = UVSim()
    sim.accum.currVal = 42
    sim.memory[0] = "+1009"
    sim.memory[1] = "+4300"
    
    # Redirect file to temp dir using monkeypatching (or tweak uvsim.py to accept filename)
    save_path = tmp_path / "uvsim_save.txt"

    # Monkeypatch the file open inside UVSim (since we can't pass custom filename to saveMemory())
    original_open = open

    def mock_open(path, mode='r', *args, **kwargs):
        if path == "uvsim_save.txt":
            return original_open(save_path, mode, *args, **kwargs)
        return original_open(path, mode, *args, **kwargs)

    # Replace built-in open temporarily
    import builtins
    builtins.open = mock_open

    try:
        result = sim.saveMemory()
        assert result == 0
        assert save_path.exists()

        with open(save_path, "r") as f:
            content = f.read()
            assert "UVSim Program" in content
            assert "Accumulator: 42" in content
            assert "00: +1009" in content
            assert "01: +4300" in content
    finally:
        # Restore the original open
        builtins.open = original_open
