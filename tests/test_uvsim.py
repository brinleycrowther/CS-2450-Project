'''
Test file for functionality of UVSim class in uvsim.py
'''

from src.uvsim import UVSim
from src.accumulator import Accumulator

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
