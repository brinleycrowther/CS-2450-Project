'''
Test file for functionality of Accumulator class in accumulator.py
'''

from accumulator import Accumulator

# Test init attributes
def test_default_values(): 
    accum = Accumulator()
    assert accum.currVal == 0
    assert accum.memory == {i:"0000" for i in range(100)}

# Test (10..) read function 
def test_read(monkeypatch):
    accum = Accumulator()
    test_inputs = iter(["1000", "+2000", "-3000"])  # iterable list for use with monkeypatch
    monkeypatch.setattr('builtins.input', lambda _: next(test_inputs))  # monkeypatch from pytest overrides input function to simulate user input

    test1 = accum.read(10, None)
    test2 = accum.read(11, None)
    test3 = accum.read(12, None)
    assert accum.memory[10] == "+1000" and test1 == "+1000"
    assert accum.memory[11] == "+2000" and test2 == "+2000"
    assert accum.memory[12] == "-3000" and test3 == "-3000"

# Test (11..) write function
def test_write(capsys):
    accum = Accumulator()
    accum.memory[1] = "+1010"   # non-default value to test

    test1 = accum.write(0, None)
    capture = capsys.readouterr()   # capsys from pytest captures printed output
    assert capture.out.strip() == "0000" and test1 == "0000"

    test2 = accum.write(1, None)
    capture = capsys.readouterr()
    assert capture.out.strip() == "+1010" and test2 == "+1010"

# Test (20..) load function
def test_load():
    accum = Accumulator()
    accum.memory[1] = "1010"    # non-default value to test

    accum.load(1, None)
    assert accum.currVal == 1010

    accum.load(0, None)
    assert accum.currVal == 0000

# Test (21..) store function
def test_store():
    accum = Accumulator()
    accum.currVal = "1010"  # value to be stored
    
    assert accum.memory[0] == "0000"    # default value
    accum.store(0, None)
    assert accum.memory[0] == "1010"

# Test (30..) add function
def test_add():
    accum = Accumulator()
    accum.memory[1] = "1000"
    accum.memory[2] = "+2000"
    accum.memory[3] = "-3000"

    assert accum.currVal == 0
    assert accum.memory[0] == "0000"
    accum.add(0, None)
    assert accum.currVal == 0
    accum.add(1, None)
    assert accum.currVal == 1000
    accum.add(2, None)
    assert accum.currVal == 3000
    accum.add(3, None)
    assert accum.currVal == 0

# Test (31..) subtract function
def test_subtract():
    accum = Accumulator()
    accum.memory[1] = "1000"
    accum.memory[2] = "+2000"
    accum.memory[3] = "-3000"

    assert accum.currVal == 0
    assert accum.memory[0] == "0000"
    accum.subtract(0, None)
    assert accum.currVal == 0
    accum.subtract(1, None)
    assert accum.currVal == -1000
    accum.subtract(2, None)
    assert accum.currVal == -3000
    accum.subtract(3, None)
    assert accum.currVal == 0

# Test (33..) divide function
def test_divide():
    accum = Accumulator()
    accum.currVal = 1000
    accum.memory[0] = "0002"
    accum.memory[1] = "+0002"
    accum.memory[2] = "-0002"

    accum.divide(0, None)
    assert accum.currVal == 500
    accum.divide(1, None)
    assert accum.currVal == 250
    accum.divide(2, None)
    assert accum.currVal == -125

# Test (34..) multiply function
def test_multiply():
    accum = Accumulator()
    accum.currVal = 10
    accum.memory[1] = "0002"
    accum.memory[2] = "+0002"
    accum.memory[3] = "-0002"

    accum.multiply(1, None)
    assert accum.currVal == 20
    accum.multiply(2, None)
    assert accum.currVal == 40
    accum.multiply(3, None)
    assert accum.currVal == -80
    accum.multiply(0, None)
    assert accum.currVal == 0
