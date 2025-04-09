'''Accumulator class. Tracks and calculates arithmetic operations'''

class Accumulator:
    def __init__(self, memory=None):
        self.currVal = 0
        if memory is None:
           self.memory = {i:"000000" for i in range(250)}  # memory location extended
        else:
            self.memory = memory

    def read(self, loc, input_word):
        while True:
            #input_word = input("Enter word: ").strip()

            # Check for sign followed by four numbers
            if input_word.startswith(("+", "-")) and len(input_word) == 7 and input_word[1:].isdigit():
                break
            # Check for four numbers
            elif len(input_word) == 6 and input_word.isdigit():
                input_word = f"+{input_word}"  # Assume positive if no sign given
                break
            else:
                return -1

        # Store the valid input into memory
        self.memory[int(loc)] = input_word
        return input_word

    #11.. WRITES word from specified location in memory(loc) and outputs it to screen
    def write(self, loc, sign):
        print(self.memory[int(loc)])
        return self.memory[int(loc)]

    # 20.. LOADS word from specific location in memory(loc) into accumulator
    def load(self, loc, sign):
        self.currVal = int(self.memory[int(loc)])

    # 21.. STORES word from accumulator into specific location in memory(loc)
    def store(self, loc, sign):
        # Format with sign and 6 digits
        sign_char = '+' if self.currVal >= 0 else '-'
        formatted_val = f"{sign_char}{abs(self.currVal):06d}"
        self.memory[int(loc)] = formatted_val

    # 30.. ADDS value from specific location in memory(loc) to accumulator currVal
    def add(self, loc, sign):
        self.currVal += int(self.memory[int(loc)])

    # 31.. SUBTRACTS value from specific location in memory(loc) from accumulator currVal
    def subtract(self, loc, sign):
        self.currVal -= int(self.memory[int(loc)])

    # 32.. DIVIDES value from specific location in memory(loc) from accumulator currVal
    def divide(self, loc, sign):
        try:
            self.currVal //= int(self.memory[int(loc)])
        except ZeroDivisionError:
            print("Error: Cannot divide by zero.")

    # 33.. MULTIPLIES value from specific location in memory(loc) to accumulator currVal
    def multiply(self, loc, sign):
        self.currVal *= int(self.memory[int(loc)])