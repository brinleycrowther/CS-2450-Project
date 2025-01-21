'''UVSim is a simulator used by computer science students to learn Basic Machine Language.
It provides a virtual environment to learn about memory, registers, and machine-level operations.
It uses four digit numbers to interpret and execute these operations.

Accumulator object instantiated in each instance of UVSim.
File passed as a string parameter into instance of UVSim.
UVSim class tracks execution log and memory. It processes each word, logs it, branches
to specific state in memory, and can be reset and saved. Both memory and execustion log can be inspected by user.
'''
from accumulator import Accumulator

class UVSim:

    def __init__(self, file=""):
        self.file = file
        self.accum = Accumulator(self.memory)
        self.log = [] # tracks log of program
        self.memory = {i: 0 for i in range(100)} # tracks and updates memory location. e.g. 00: +1234

    # grabs word from file, splits sign, splits first two digits(function) from last two digits(value)
    # uses accumulator functions to process the word
    # if file == "" ask for input again, or if file != .txt throw error ask for file input
    def wordProcess(self):
        if self.file == "":
            self.file = input("Which file would you like to run?\n")
            self.wordProcess()
        elif (self.file[-4] + self.file[-3] + self.file[-2] + self.file[-1]) != ".txt":
            print("File type invalid.")
            self.file = input("Which file would you like to run?\n")
            self.wordProcess()
        else:
            lineNum = 0 # tracks line number in file for error messages
            with open(self.file, 'r') as file: # reads file
                words = file.readlines()
                for word in words:
                    lineNum += 1 # increments line number for each word
                    if len(word) != 6 or len(word) != 5: # ensures each line has a sign, operation, and memory location (+ new line)
                        print(f'Word invalid on line {lineNum}')
                        break
                    else:
                        if word[0] == '+' or word[0] == '-':
                            sign = word[0] # sign is first char in word
                            operation = word[1] + word[2] # operation is next two chars
                            location = word[3] + word[4] # location in memory is last two chars
                        else: # we can assume word is positive if not specified
                            sign = '+'
                            operation = word[0] + word[1]
                            location = word[2] + word[3]

                        # takes OpCode and passes location and sign of word to its function
                        if operation == "10":
                            self.accum.read(location, sign)
                        elif operation == "11":
                            self.accum.write(location, sign)
                        elif operation == "20":
                            self.accum.load(location, sign)
                        elif operation == "21":
                            self.accum.store(location, sign)
                        elif operation == "30":
                            self.accum.add(location, sign)
                        elif operation == "31":
                            self.accum.subtract(location, sign)
                        elif operation == "32":
                            self.accum.divide(location, sign)
                        elif operation == "33":
                            self.accum.multiply(location, sign)
                        elif operation == "40":
                            self.branch(location)
                        elif operation == "41":
                            self.branchneg(location)
                        elif operation == "42":
                            self.branchzero(location)
                        elif operation == "43":
                            self.halt()
                        else:
                            print(f'Word on line {lineNum} contains OpCode that does not exist.')
                            break


    # 40.. jumps to specified state in memory(value) and starts counter
    def branch(self, value):
        pass

    # 41.. jumps to specified state in memory(value) if accumulator is negative and starts counter
    def branchneg(self, value):
        pass
    
    # 42.. jumps to specified state in memory(value) if accumulator is zero and starts counter
    def branchzero(self, value):
        pass

    # stops program counter
    def halt(self, value):
        pass

    # fetches current state of accumulator. currVal, current instruction, and program counter
    def inspectCurrent(self):
        pass

    # displays all memory content. eg 00: +1234
    def inspectMemory(self):
        pass

    # displays log
    def logDisplay(self):
        pass

    # writes memory accumulator, and counter values into .txt file
    def saveState(self):
        pass
    
    # sets self.file to file specified
    def loadState(self):
        pass

    # resets accumulator to 0 and memory to 00
    def reset(self):
        pass

def main():
    inputFile = input("Which file would you like to run?\n") # asks for file to load
    program = UVSim()
    program.wordProcess()

if __name__ == '__main__':
    main()