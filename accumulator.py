'''Accumulator class. Tracks and calculates arithemitic operations'''

class Accumulator:
    def __init__(self, memory):
       self.currVal = 0
       self.memory = memory

    # 10.. READS word from input and puts into specifiec memory location(loc)
    def read(self, loc, sign):
        pass

    #11.. WRITES word from specified location in memory(loc) and outputs it to screen
    def write(self, loc, sign):
        pass

    # 20.. LOADS word from specific location in memory(loc) into accumulator
    def load(self, loc, sign):
        pass

    # 21.. STORES word from accumulator into specific location in memory(loc)
    def store(self, loc, sign):
        pass

    # 30.. ADDS value from specific location in memory(loc) to accumulator currVal
    def add(self, loc, sign):
        pass

    # 31.. SUBTRACTS value from specific location in memory(loc) from accumulator currVal
    def subtract(self, loc, sign):
        pass

    # 32.. DIVIDES value from specific location in memory(loc) from accumulator currVal
    def divide(self, loc, sign):
        pass

    # 33.. MULTIPLIES value from specific location in memory(loc) to accumulator currVal
    def multiply(self, loc, sign):
        pass