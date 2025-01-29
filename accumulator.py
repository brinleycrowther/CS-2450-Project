'''Accumulator class. Tracks and calculates arithemitic operations'''

class Accumulator:
    def __init__(self, memory):
       self.currVal = 0
       self.memory = memory

    # 10.. READS word from input and puts into specifiec memory location(loc)
    def read(self, loc, sign):
        invalid_input = True
        while invalid_input:
            input_word = str(input('Enter word: '))
            if (input_word[0] != '+' and input_word[0] != '-') and len(input_word) != 4:
            #if len(input_word) > 6 or len(input_word) < 5: # ensures each line has a sign, operation, and memory location (+ new line)
                print(f'Invalid word')
            elif (input_word[0] == '+' or input_word[0] == '-') and len(input_word) != 5:
                print(f'Invalid word')
            else:
                invalid_input = False
                if input_word[0] == '+' or input_word[0] == '-':
                    #print(f"Putting word {input_word} in location {int(loc)}; type of loc: {type(loc)}")
                    self.memory[int(loc)] = input_word
                    return input_word

                else: # we can assume word is positive if not specified
                    self.memory[int(loc)] = f"+{input_word}"
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