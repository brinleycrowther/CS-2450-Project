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
        self.memory = {i: "000000" for i in range(250)} # tracks and updates memory location. e.g. 00: +123456 and memory limit of 250 lines
        self.accum = Accumulator(self.memory)
        self.record = True

    # asks for file. validates file. proccesses each word into memory
    def fileInputToMemory(self, inputFile):
        if inputFile and os.path.exists(inputFile):
            lineNum = 0 # tracks line number in file for error messages
            try:
                with open(inputFile, 'r') as file: # reads file
                    words = file.readlines()
                    if len(words) > 250:
                        self.update_console("Error: File contains more than 250 lines.")  # Rejects 250-line files
                        return -1
                    
                    for word in words:
                        word = word.strip('\n')
                        lineNum += 1 # increments line number for each word
                        
                        digits = self.detect_format(word)
                        if digits == 4:
                            word = self.convert_to_six_digts(word)

                        # loads each word into corresponding memory space    
                        self.memory[self.memSpace] = word
                        self.memSpace += 1
                
                self.update_console(f"Loaded file {inputFile} into memory.")
                self.log.append(f'File {inputFile} loaded into memory')
                Clock.schedule_once(lambda dt: self.ui.update_program_counter(self.counter)) # updtes program counter in ui
                self.ui.refresh_memory_table(0)
                Clock.schedule_once(lambda dt: self.ui.update_accumulator(self.getAccumulator())) # updates accumulator with current value
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
        print(f"Executing instruction at {self.counter}: {self.memory[self.counter]}")

        if self.counter >= 250:
            self.update_console("Error: Program counter out of bounds (000-249).")  # Prevents execution from going beyond the valid memory range

        if len(self.log) > 0 and self.log[-1] == "+430000 : Program halted":
            self.update_console("Program halted.\nPress save to save state to a text file, and Quit to exit.")
            return
        
        # goes through each space in memory and processes the word
        while self.counter < self.memSpace:
            #self.ui.refresh_memory_table(self.counter - 1)
            value = self.memory[self.counter]
            self.counter += 1
            
            # Updated parsing logic for 6-digit format
            sign = value[0] if value[0] in ('+', '-') else '+'
            operation = value[1:4]  # Directly extract 3 digits for operation code
            location = int(value[4:])    # Extract remaining 3 digits for memory address

            if location < 0 or location >= 250:
                self.update_console(f"Error: Invalid memory reference {location} (must be 000-249).")  # instructions only reference valid memory addresses (000-249)
                return

            # takes OpCode and passes location and sign of word to its function
            if operation == "010":
                self.update_console("Enter word into Console Input, then press Enter.")
                self.ui.focus_console_input()
                self.ui.refresh_memory_table(highlight_index=(self.counter-1))
                self.waiting_for_input = [location, value, step]
                return # makes program wait for input
            elif operation == "011":
                self.log.append(f'{value} : {self.accum.write(location, sign)} output from {location} in memory onto terminal')
            elif operation == "020":
                self.accum.load(location, sign)
                self.log.append(f'{value} : {self.memory[int(location)]} loaded into accumulator')
            elif operation == "021":
                self.accum.store(location, sign)
                self.log.append(f'{value} : {self.memory[int(location)]} stored into {location} in memory')
            elif operation == "030":
                self.accum.add(location, sign)
                self.log.append(f'{value} : Accumulator added to {self.memory[int(location)]} from {location} in memory')
            elif operation == "031":
                self.accum.subtract(location, sign)
                self.log.append(f'{value} : Accumulator subtracted by {self.memory[int(location)]} from {location} in memory')
            elif operation == "032":
                self.accum.divide(location, sign)
                self.log.append(f'{value} : Accumulator divded by {self.memory[int(location)]} from {location} in memory')
            elif operation == "033":
                self.accum.multiply(location, sign)
                self.log.append(f'{value} : Accumulator multiplied by {self.memory[int(location)]} from {location} in memory')
            elif operation == "040":
                self.branch(location)
            elif operation == "041":
                self.branchneg(location)
            elif operation == "042":
                self.branchzero(location)
            elif operation == "043":
                self.update_console(f'{value} : Program halted.\nPress Save to save current memory to a text file, and Quit to exit.')
                self.log.append(f'{value} : Program halted')
                Clock.schedule_once(lambda dt: self.ui.update_program_counter(self.counter-1))
                self.ui.refresh_memory_table(highlight_index=(self.counter-1))
                Clock.schedule_once(lambda dt: self.ui.update_accumulator(self.getAccumulator())) # updates to current accumulator value
                self.ui.make_reset_button()
                return
            else:
                self.log.append(f'Word: {value} in memory space {self.counter} is inoperable.')

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
            print(read_return)
            #read_return = self.convert_to_six_digts(read_return)
            if read_return == -1:
                self.update_console("Invalid word.")
                self.counter -= 1 # decrements counter to reprocess word
                self.wordProcess(step) # resumes execution
                return
            else:
                self.log.append(f'{value} : {read_return} read into {location} in memory')

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
        Clock.schedule_once(lambda dt: self.ui.update_program_counter(self.counter - 1)) # updtes program counter in ui
        self.ui.refresh_memory_table(self.counter - 1)
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
            curr = f'Program\'s current state:\nAccumulator: {self.accum.currVal}\nAction: No instructions loaded'
        else:
            curr = f'Program\'s current state:\nAccumulator: {self.accum.currVal}\nAction: {self.log[-1]}'
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
            # Format with sign and leading zeros (like memory values)
            sign = '+' if self.accum.currVal >= 0 else '-'
            return f"{sign}{abs(self.accum.currVal):06d}"  # Outputs "+001801" instead of "1801"
        
    # outputs accumulator value and memory into .txt file
    def saveMemory(self, file_path):
        try:
            with open(file_path, 'w') as file:
                file.write("UVSim Program\n\n")
                file.write(f'Accumulator: {self.accum.currVal}\n\n')
                file.write(f'Memory:\n')
                for location, value in self.memory.items():
                    if location < 10:
                        file.write(f'0{location}: {value}\n')
                    else:
                        file.write(f'{location}: {value}\n')

            self.update_console(f"State saved to {file_path}")
            return 0     
           
        except Exception as e:
            self.update_console(f'Error saving state: {e}')
            return -1

    # outputs text into console
    def update_console(self, message):
        Clock.schedule_once(lambda dt: self.ui.console_insert_text(message))

    # resets program
    def reset(self):
        self.log.append("Program reset.")
        self.memSpace = 0
        self.counter = 0
        self.memory = {i: "000000" for i in range(250)} # update to 6 digits & 250 memory
        self.accum = Accumulator(self.memory)

    # quits program
    def quit(self):
        App.get_running_app().stop()
        Window.close()
        exit()

    # converts word to 6 digits
    def convert_to_six_digts(self, word):
        """Converts 4-digit words to 6-digit format."""
        has_sign = len(word) > 0 and word[0] in '+-'
        if (has_sign and len(word) == 5) or (not has_sign and len(word) == 4):
            sign = word[0] if has_sign else '+'
            digits = word[1:] if has_sign else word
            digits = digits.ljust(4, '0')[:4]  # Ensure 4 digits, pad if needed
            opcode = digits[:2].zfill(3)  # First two digits as opcode, pad to 3
            address = digits[2:].zfill(3)  # Last two as address, pad to 3
            return f"{sign}{opcode}{address}"
        return word

    # Add the save_converted_program method in the UVSim class
    def save_converted_program(self, file_path):
        """Saves the converted 6-digit program to a file."""
        try:
            with open(file_path, 'w') as file:
                for loc in range(self.memSpace):
                    word = self.memory[loc]
                    file.write(f"{word}\n")
            self.update_console(f"Converted program saved to {file_path}")
            return 0
        except Exception as e:
            self.update_console(f'Error saving converted program: {e}')
            return -1
    
    # detects how many digits the word is
    def detect_format(self, line):
        length = len(line.strip())
        if length == 4 or length == 5:
            return 4
        elif length == 6 or length == 7:
            return 6
        else:
            raise ValueError(f"{line} contains an invalid number of digits.")

class MyUVSimApp(App):
    def build(self):
        ui = UVSimUI()
        simulator = UVSim(ui)

        return ui

if __name__ == '__main__':
    MyUVSimApp().run() # starts UI
