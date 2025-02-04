'''
Test file for functionality of UVSim class in uvsim.py
'''

from uvsim import UVSim
from accumulator import Accumulator

# Test UVSim initialization
def test_default_values():
    sim = UVSim()
    assert sim.file == ""
    assert sim.log == []
    assert sim.state == 0
    assert sim.memory == {i:"0000" for i in range(100)}
    assert isinstance(sim.accum, Accumulator)
    assert sim.record

# Test (40..) branch function
def test_branch():
    sim = UVSim()
    sim.branch(10)
    assert sim.state == 10
    assert sim.log[-1] == "4010 : Program branch to 10"

# Test (41..) branchneg function
def test_branchneg():
    sim = UVSim()
    
    sim.branchneg(10)   # test branch fail condition
    assert sim.state == 0
    assert sim.record is False

    sim.accum.currVal = -1  # test successful branch condition
    sim.branchneg(10)
    assert sim.state == 10
    assert sim.log[-1] == "4110 : Program branch to 10"

# Test (42..) branchzero function
def test_branchzero():
    sim = UVSim()

    sim.branchzero(10)  # test successful branch condition
    assert sim.state == 10
    assert sim.log[-1] == "4210 : Program branch to 10"

    sim.accum.currVal = 1   # test branch fail condition
    sim.branchzero(20)
    assert sim.state == 10
    assert sim.record is False

# Test inspectCurrent function
def test_inspectCurrent():
    sim = UVSim()
    assert sim.inspectCurrent() == "Program's current state:\nAccumulator: 0\nCurrent instruction: 0000\nProgram counter: 0"

    sim.accum.currVal = 10
    sim.state = 1
    sim.memory[0] = 1010
    assert sim.inspectCurrent() == "Program's current state:\nAccumulator: 10\nCurrent instruction: 1010\nProgram counter: 1"
