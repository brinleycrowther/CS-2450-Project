'''Accumulator class. Tracks and calculates arithmetic operations'''

class Accumulator:
    def __init__(self, memory=None):
        self.currVal = 0
        if memory is None:
           self.memory = {i:"0000" for i in range(100)}
        else:
            self.memory = memory

    def read(self, loc, sign):
        while True:
            input_word = input("Enter word: ").strip()

            # Check for sign followed by four numbers
            if input_word.startswith(("+", "-")) and len(input_word) == 5 and input_word[1:].isdigit():
                break
            # Check for four numbers
            elif len(input_word) == 4 and input_word.isdigit():
                input_word = f"+{input_word}"  # Assume positive if no sign given
                break
            else:
                print("Invalid word")

        # Store the valid input into memory
        self.memory[int(loc)] = input_word
        return input_word

    #11.. WRITES word from specified location in memory(loc) and outputs it to screen
    def write(self, loc, sign):
        print(self.memory[int(loc)])
        #print(f"11: writes {self.memory[int(loc)]} from {int(loc)} to screen")
        return self.memory[int(loc)]

    # 20.. LOADS word from specific location in memory(loc) into accumulator
    def load(self, loc, sign):
        self.currVal = int(self.memory[int(loc)])
        #print(f"20: loads {self.memory[int(loc)]} to accumulater: {self.currVal}")

    # 21.. STORES word from accumulator into specific location in memory(loc)
    def store(self, loc, sign):
        self.memory[int(loc)] = str(self.currVal)
        #print(f"21: stores accumulator {self.currVal} into {int(loc)}")

    # 30.. ADDS value from specific location in memory(loc) to accumulator currVal
    def add(self, loc, sign):
        self.currVal += int(self.memory[int(loc)])
        #print(f"30: adds {self.memory[int(loc)]} to accumulator {self.currVal}")

    # 31.. SUBTRACTS value from specific location in memory(loc) from accumulator currVal
    def subtract(self, loc, sign):
        self.currVal -= int(self.memory[int(loc)])
        #print(f"31: subtracts {self.memory[int(loc)]} from accumulator {self.currVal}")

    # 32.. DIVIDES value from specific location in memory(loc) from accumulator currVal
    def divide(self, loc, sign):
        self.currVal /= int(self.memory[int(loc)])
        #print(f"32: divides {self.memory[int(loc)]} from accumulator {self.currVal}")

    # 33.. MULTIPLIES value from specific location in memory(loc) to accumulator currVal
    def multiply(self, loc, sign):
        self.currVal *= int(self.memory[int(loc)])
        #print(f"33: multiplies {self.memory[int(loc)]} to accumulator {self.currVal}")