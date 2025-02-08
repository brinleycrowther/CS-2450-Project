# **Testing Documentation**

## Unit Tests for UVSim.py and Accumulator.py

This doc contains information pertaining to all unit testing for the CS 2450 Team 5 Group Project. Included are instructions for execution and a table with executable tests, brief descriptions, references to use cases, and success/fail conditions.

### Instructions to Run Test Files
---   
Unit testing utilizes Pytest to run automated test files. These files are named `test_uvsim.py` and `test_accumulator.py`.  

To run tests from terminal, execute the pytest command within the same directory as the test files:
```python
pytest
```

### Pytest Run Results and Expected Output
---

Pytest uses `assert` to automatically test and confirm the state or output of program as functionality test code runs. After being run, Pytest will display testing results in the terminal. Unit test results are displayed on function-basis. Any failed assertions will be displayed in red, along with line numbers to specify what assertion failed. Upon 100% successful tests, no functions will be shown.  

Each function test listed in the tables below contains multiple assertion tests within for default values, modified values, and conditional changes. Desired output is 100% successful tests.

### UVSim Test Reference Table
---

|Test Name|Description|Use Case|Conditions|  
|-|-|-|-|
|`test_default_values()`|Tests UVSim object initialization|Create any instance of UVSim|Asserts all intended default attribute values|  
|`test_branch()`|Tests operation code 40.. branch functionality|Instruction pointer jumps to specified location|Asserts state attribute changes to given memory index|  
|`test_branchneg()`|Tests operation code 41.. branch functionality|Instruction pointer jumps to specified location conditionally|Asserts state attribute changes to given memory index when, and only when `UVSim.memory.currVal` is a negative value|  
|`test_branchzero()`|Tests operation code 42.. branch functionality|Instruction pointer jumps to specified location conditionally|Asserts state attribute changes to given memory index when, and only when `UVSim.memory.currVal` is zero|  
|`test_inspectCurrent()`|Tests UVSim function for correct display of information|Displays vital information about object attributes for runtime debugging|Asserts correct display of information in default state, as well as after attribute data manipulation|  

### Accumulator Test Reference Table
---

|Test Name|Description|Use Case|Conditions|  
|-|-|-|-|
|`test_default_values()`|Tests Accumulator object initialization|Create any instance of Accumulator|Asserts all intended default attribute values|  
|`test_read()`|Tests operation code 10.. input reading functionality|Input is retrieved from user and placed in specified memory location|Asserts proper placement in memory for 4 digit inputs, with or without + or - signs|
|`test_write()`|Tests operation code 11.. writing to terminal functionality|Word from memory is displayed to the user|Asserts correct system output for default and modified values|  
|`test_load()`|Tests operation code 20.. load Accumulator register functionality|The Accumulator register is overwritten with a value from memory|Asserts correct `Accumulator.currVal` values after loading default and modified memory|  
|`test_store()`|Tests operation code 21.. store Accumulator register functionality|Value of `Accumulator.currVal` is stored into specified memory index|Asserts that default memory changes to register value, and register value does not change|  
|`test_add()`|Tests operation code 30.. add arithmetic functionality|The value of `Accumulator.currVal` is added to a specified value in memory and the sum is stored in the register|Asserts proper sum functionality with positive, negative, and no-sign values|  
|`test_subtract()`|Tests operation code 31.. subtract arithmetic functionality|The value in a specified memory location is subtracted from `Accumulator.currVal` and the result is stored in the register|Asserts proper subtraction functionality with positive, negative, and no-sign values|  
|`test_divide()`|Tests operation code 32.. divide arithmetic functionality|The value in a specified memory location is divided from `Accumulator.currVal` and the result is stored in the register|Asserts proper division functionality with positive, negative, and no-sign values. Manual test of division by zero raises error.|  
|`test_multiply()`|Tests operation code 33.. multiply arithmetic functionality|The value of `Accumulator.currVal` is multiplied by a specified value in memory and the result is stored in the register|Asserts proper multiplication functionality with positive, negative, and no-sign values|  

### Additional Manual Testing
---

Additional comprehensive testing was completed manually by curating custom test files with known desired outputs. These tests were run using IDE step-by-step debugging tools to confirm proper code flow, values, and operations. Output files were directly compared with predetermined desired output for confirmation of accuracy.