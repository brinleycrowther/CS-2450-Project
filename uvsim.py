'''UVSim is a simulator used by computer science students to learn Basic Machine Language.
It provides a virtual environment to learn about memory, registers, and machine-level operations.
It uses four digit numbers to interpret and execute these operations.

Accumulator object instantiated in each instance of UVSim.
File passed as a string parameter into instance of UVSim.
UVSim class tracks execution log and memory. It processes each word, logs it, branches
to specific state in memory, and can be reset and saved. Both memory and execution log can be inspected by user.
'''
from accumulator import Accumulator
from pathlib import Path # used to check if file is in path
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
import os
from uvsim_gui import UVSimUI

class UVSim:
    def __init__(self, ui = None):
        self.ui = ui # reference to ui
        self.log = [] # tracks log of program
        self.memSpace = 0 # where program counter will continue
        self.counter = 0 # tracks where in what word is being processed in memory
        self.memory = {i: "0000" for i in range(100)} # tracks and updates memory location. e.g. 00: +1234
        self.accum = Accumulator(self.memory)
        self.record = True

    # asks for file. validates file. proccesses each word into memory
    def fileInputToMemory(self, inputFile):
        if inputFile and os.path.exists(inputFile):
            lineNum = 0 # tracks line number in file for error messages
            try:
                with open(inputFile, 'r') as file: # reads file
                    words = file.readlines()
                    for word in words:
                        word = word.strip('\n')
                        lineNum += 1 # increments line number for each word

                        # loads each word into corresponding memory space    
                        self.memory[self.memSpace] = word
                        self.memSpace += 1
                
                self.update_console("Loaded file!")
                return 0
            except Exception as e:
                self.update_console(f'Error opening file: {e}')
                return -1
        else:
            self.update_console("Invalid file.")
            return -1
    
    # grabs word from file, splits sign, splits first two digits(function) from last two digits(value)
    # uses accumulator functions to process the word
    def wordProcess(self, step = False):
        if len(self.log) > 0 and self.log[-1] == "+4300 : Program halted":
            self.update_console("Program halted.\nPress save to save state to a text file, and Quit to exit.")
            return

        # goes through each space in memory and processes the word
        while self.counter < self.memSpace:
            value = self.memory[self.counter]
            self.counter += 1
            sign = value[0] if value[0] in ('+', '-') else '+'
            operation = value[1:3] if sign in ('+', '-') else value[:2]
            location = value[3:] if sign in ('+', '-') else value[2:]

            # takes OpCode and passes location and sign of word to its function
            if operation == "10":
                self.update_console("Enter word into Console Input, then press Enter.")
                self.ui.focus_console_input()
                self.waiting_for_input = [location, value, step]
                return # makes program wait for input
            elif operation == "11":
                self.log.append(f'{value} : {self.accum.write(location, sign)} output from {location} in memory onto terminal')
            elif operation == "20":
                self.accum.load(location, sign)
                self.log.append(f'{value} : {self.memory[int(location)]} loaded into accumulator')
            elif operation == "21":
                self.accum.store(location, sign)
                self.log.append(f'{value} : {self.memory[int(location)]} stored into {location} in memory')
            elif operation == "30":
                self.accum.add(location, sign)
                self.log.append(f'{value} : Accumulator added to {self.memory[int(location)]} from {location} in memory')
            elif operation == "31":
                self.accum.subtract(location, sign)
                self.log.append(f'{value} : Accumulator subtracted by {self.memory[int(location)]} from {location} in memory')
            elif operation == "32":
                self.accum.divide(location, sign)
                self.log.append(f'{value} : Accumulator divded by {self.memory[int(location)]} from {location} in memory')
            elif operation == "33":
                self.accum.multiply(location, sign)
                self.log.append(f'{value} : Accumulator multiplied by {self.memory[int(location)]} from {location} in memory')
            elif operation == "40":
                self.branch(location)
            elif operation == "41":
                self.branchneg(location)
            elif operation == "42":
                self.branchzero(location)
            elif operation == "43":
                self.update_console(f'{value} : Program halted.\nPress Save to save current state to a text file, and Quit to exit.')
                self.log.append(f'{value} : Program halted')
                Clock.schedule_once(lambda dt: self.ui.update_accumulator(self.getAccumulator())) # updates to current accumulator value
                return
            else:
                self.log.append(f'Word: {value} in memory space {self.counter} is inoperable.')

            self.ui.refresh_memory_table()
            if step and len(self.log) > 0:
                self.stepProgram()
                return

    # takes input from ui to use in logic
    def process_input(self, input_word):
        if self.waiting_for_input:
            location = self.waiting_for_input[0]
            value = self.waiting_for_input[1]
            step = self.waiting_for_input[2]
            self.waiting_for_input = None  # Clear state

            read_return = self.accum.read(location, input_word)
            if read_return == -1:
                self.update_console("Invalid word.")
                self.counter -= 1 # decrements counter to reprocess word
                self.wordProcess(step) # resumes execution
                return
            else:
                self.log.append(f'{value} : {read_return} read into {location} in memory')
                self.ui.refresh_memory_table()

                # resumes execution
                if step == True:
                    self.stepProgram()
                    return
                self.wordProcess(step)

    # displays memory and current state, breaks function when enter is pressed
    def stepProgram(self):
        '''stepInput = input("Would you like to run the program step by step? y/n\n")
        if stepInput.lower() == 'y':
            self.step = True
        elif stepInput.lower() == 'n':
            self.step = False
        else:
            raise ValueError("Input invalid. Must be y or n.")'''
        
        #self.inspectMemory()
        #contInput = input("Press enter to continue")
        self.update_console(self.log[-1])
        Clock.schedule_once(lambda dt: self.ui.update_accumulator(self.getAccumulator())) # updates accumulator with current value
        return

    # 40.. jumps to specified state in memory(value) and starts counter
    def branch(self, value):
        self.counter = int(value)
        self.log.append(f'+40{value} : Program branch to {value}')
        return self.memSpace

    # 41.. jumps to specified state in memory(value) if accumulator is negative and starts counter
    def branchneg(self, value):
        if self.accum.currVal < 0:
            self.counter = int(value)
            self.log.append(f'+41{value} : Program branch to {value}')
        else:
            self.log.append(f'+41{value} : Program branch to {value} failed')
        return self.memSpace
    
    # 42.. jumps to specified state in memory(value) if accumulator is zero and starts counter
    def branchzero(self, value):
        if self.accum.currVal == 0:
            self.counter = int(value)
            self.log.append(f'+42{value} : Program branch to {value}')
        else:
            self.log.append(f'+42{value} : Program branch to {value} failed')
        return self.memSpace

    # fetches current state of accumulator. currVal, current instruction, and program counter
    def inspectCurrent(self):
        if self.memSpace == 0:
            curr = f'Program\'s current state:\nAccumulator: {self.accum.currVal}\nAction: {self.log[self.memSpace]}'
        else:
            curr = f'Program\'s current state:\nAccumulator: {self.accum.currVal}\nAction: {self.log[self.counter - 1]}'
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
        #print("Program log:")
        for item in self.log:
            print(item)
        return self.log
    
    # shows accumulator state
    def getAccumulator(self):
        if self.accum.currVal == 0:
            return "No value in accumulator..."
        else:
            return str(self.accum.currVal)
    
    # outputs accumulator value and memory into .txt file
    def saveMemory(self):
        try:
            with open("uvsim_save.txt", 'w') as file:
                file.write("UVSim Program\n\n")
                file.write(f'Accumulator: {self.accum.currVal}\n\n')
                file.write(f'Memory:\n')
                for location, value in self.memory.items():
                    if location < 10:
                        file.write(f'0{location}: {value}\n')
                    else:
                        file.write(f'{location}: {value}\n')

            self.update_console("State saved to uvsim_save.txt")
            return 0     
           
        except Exception as e:
            self.update_console(f'Error saving state: {e}')
            return -1

    # outputs text into console
    def update_console(self, message):
        Clock.schedule_once(lambda dt: self.ui.console_insert_text(message))

    # quits program
    def quit(self):
        App.get_running_app().stop()
        Window.close()
        exit()

class MyUVSimApp(App):
    def build(self):
        ui = UVSimUI()
        simulator = UVSim(ui)

        return ui

if __name__ == '__main__':
    MyUVSimApp().run() # starts UI
