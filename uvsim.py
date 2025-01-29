'''UVSim is a simulator used by computer science students to learn Basic Machine Language.
It provides a virtual environment to learn about memory, registers, and machine-level operations.
It uses four digit numbers to interpret and execute these operations.

Accumulator object instantiated in each instance of UVSim.
File passed as a string parameter into instance of UVSim.
UVSim class tracks execution log and memory. It processes each word, logs it, branches
to specific state in memory, and can be reset and saved. Both memory and execustion log can be inspected by user.
'''
from accumulator import Accumulator
from pathlib import Path # used to check if file is in path

class UVSim:
    def __init__(self, file=""):
        self.file = file
        self.log = [] # tracks log of program
        self.state = 0 # where program counter will continue
        self.memory = {i: 0 for i in range(100)} # tracks and updates memory location. e.g. 00: +1234
        self.accum = Accumulator(self.memory)
        self.record = True

    # grabs word from file, splits sign, splits first two digits(function) from last two digits(value)
    # uses accumulator functions to process the word
    # if file == "" ask for input again, or if file != .txt throw error ask for file input
    def wordProcess(self):
        if self.file == "":
            self.file = input("Which file would you like to run?\n")
            self.wordProcess()
        elif (self.file[-4] + self.file[-3] + self.file[-2] + self.file[-1]) != ".txt": # makes sure file is a .txt
            print("File type invalid.")
            self.file = input("Which file would you like to run?\n")
            self.wordProcess()
        elif Path(self.file).exists() == False: # makes sure file is in path
            print("File does not exist in folder.")
            self.file = input("Which file would you like to run?\n")
            self.wordProcess()
        else:
            lineNum = 0 # tracks line number in file for error messages
            with open(self.file, 'r') as file: # reads file
                words = file.readlines()
                for word in words:
                    lineNum += 1 # increments line number for each word
                    if len(word) != 6 and len(word) != 5: # ensures each line has a sign, operation, and memory location (+ new line)
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
                            self.log.append(f'{self.accum.read(location, sign)} read into {location} in memory')
                        elif operation == "11":
                            self.log.append(f'{self.accum.write(location, sign)} output from {location} in memory onto screen')
                        elif operation == "20":
                            self.accum.load(location, sign)
                            self.log.append(f'{self.memory[int(location)]} loaded into accumulator')
                        elif operation == "21":
                            self.accum.store(location, sign)
                            self.log.append(f'{self.memory[int(location)]} stored into {location} in memory')
                        elif operation == "30":
                            self.accum.add(location, sign)
                            self.log.append(f'Accumulator added to {self.memory[int(location)]} from {location} in memory')
                        elif operation == "31":
                            self.accum.subtract(location, sign)
                            self.log.append(f'Accumulator subtracted from {self.memory[int(location)]} from {location} in memory')
                        elif operation == "32":
                            self.accum.divide(location, sign)
                            self.log.append(f'Accumulator divded by {self.memory[int(location)]} from {location} in memory')
                        elif operation == "33":
                            self.accum.multiply(location, sign)
                            self.log.append(f'Accumulator multiplied by {self.memory[int(location)]} from {location} in memory')
                        elif operation == "40":
                            self.branch(location)
                        elif operation == "41":
                            self.branchneg(location)
                        elif operation == "42":
                            self.branchzero(location)
                        elif operation == "43":
                            print("Program halted.")
                            self.log.append("Program halted")
                            self.memory[self.state] = word.strip('\n')
                            break
                        else:
                            print(f'Word on line {lineNum} contains OpCode that does not exist.')
                            break
                        
                        if self.record == True:
                            self.memory[self.state] = word.strip('\n')
                            self.state += 1
                        else:
                            self.record = True


    # 40.. jumps to specified state in memory(value) and starts counter
    def branch(self, value):
        self.state = int(value)
        self.log.append(f'Program branch to {value}')
        return self.state

    # 41.. jumps to specified state in memory(value) if accumulator is negative and starts counter
    def branchneg(self, value):
        if self.accum.currVal < 0:
            self.state = int(value)
            self.log.append(f'Program branch to {value}')
        else:
            self.record = False
        return self.state
    
    # 42.. jumps to specified state in memory(value) if accumulator is zero and starts counter
    def branchzero(self, value):
        if self.accum.currVal == 0:
            self.state = int(value)
            self.log.append(f'Program branch to {value}')
        else:
            self.record = False
        return self.state

    # fetches current state of accumulator. currVal, current instruction, and program counter
    def inspectCurrent(self):
        curr = f'Program\'s current state:\nAccumulator: {self.accum.currVal}\nCurrent instruction: {self.memory[self.state - 1]}\nProgram counter: {self.state}'
        return curr

    # displays all memory content. eg 00: +1234
    def inspectMemory(self):
        for location, value in self.memory.items():
            if location < 10:
                print(f'0{location}: {value}')
            else:
                print(f'{location}: {value}')

    # displays log
    def logDisplay(self):
        print("Program log:")
        for item in self.log:
            print(item)
        return self.log
    
    # shows accumulator state
    def displayAccumulator(self):
        return f'Accumulator: {self.accum.currVal}'
    
    # outputs accumulator value and memory into .txt file
    def saveState(self):
        fileSave = input("File name:\n")

        if fileSave[-4] != '.':
            fileSave += ".txt"

        with open(fileSave, 'w') as file:
            file.write("UVSim Program\n\n")
            file.write(f'Accumulator: {self.accum.currVal}\n\n')
            file.write(f'Memory:\n')
            for location, value in self.memory.items():
                if location < 10:
                    file.write(f'0{location}: {value}\n')
                else:
                    file.write(f'{location}: {value}\n')
def main():
    inputFile = input("Which file would you like to run?\n") # asks for file to load
    program = UVSim(inputFile)
    program.wordProcess()
    program.inspectMemory()
    program.logDisplay()
    program.saveState()

if __name__ == '__main__':
    main()