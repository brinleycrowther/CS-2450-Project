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

|Test Name|Description|Use Case|Inputs|Output|Conditions of Success/Fail|  
|-|-|-|-|
|`test_default_values()`|Tests UVSim object initialization|N/A|N/A|N/A|Asserts all intended default attribute values|  
|`test_branch()`|Tests operation code 40.. branch functionality|UC4|N/A|N/A|Asserts state attribute changes to given memory index|  
|`test_branchneg()`|Tests operation code 41.. branch functionality|UC4|N/A|N/A|Asserts state attribute changes to given memory index when, and only when `UVSim.memory.currVal` is a negative value|  
|`test_branchzero()`|Tests operation code 42.. branch functionality|UC4|N/A|N/A|Asserts state attribute changes to given memory index when, and only when `UVSim.memory.currVal` is zero|  
|`test_inspectCurrent()`|Tests UVSim function for correct display of information|UC7|N/A|Most recently added log string|Asserts correct display of information in default state, as well as after attribute data manipulation|  

### Accumulator Test Reference Table
---

|Test Name|Description|Use Case|Inputs|Outputs|Conditions of Success/Fail|  
|-|-|-|-|
|`test_default_values()`|Tests Accumulator object initialization|N/A|N/A|N/A|Asserts all intended default attribute values|  
|`test_read()`|Tests operation code 10.. input reading functionality|UC1|A 4 digit "word", with or without a pos/neg sign|N/A|Asserts proper placement in memory for 4 digit inputs, with or without + or - signs|
|`test_write()`|Tests operation code 11.. writing to terminal functionality|UC2|Memory location|Word from memory displayed as string|Asserts correct system output for default and modified values|  
|`test_load()`|Tests operation code 20.. load Accumulator register functionality|UC3|Value from memory|N/A|Asserts correct `Accumulator.currVal` values after loading default and modified memory|  
|`test_store()`|Tests operation code 21.. store Accumulator register functionality|UC3|N/A|N/A|Asserts that default memory changes to register value, and register value does not change|  
|`test_add()`|Tests operation code 30.. add arithmetic functionality|UC3|Memory location|N/A|Asserts proper sum functionality with positive, negative, and no-sign values|  
|`test_subtract()`|Tests operation code 31.. subtract arithmetic functionality|UC3|Memory location|N/A|Asserts proper subtraction functionality with positive, negative, and no-sign values|  
|`test_divide()`|Tests operation code 32.. divide arithmetic functionality|UC3|Memory location|N/A|Asserts proper division functionality with positive, negative, and no-sign values. Manual test of division by zero raises error.|  
|`test_multiply()`|Tests operation code 33.. multiply arithmetic functionality|UC3|Memory location|N/A|Asserts proper multiplication functionality with positive, negative, and no-sign values|  

### Additional Manual Testing
---

Additional comprehensive testing was completed manually by curating custom test files with known desired outputs. These tests were run using IDE step-by-step debugging tools to confirm proper code flow, values, and operations. Output files were directly compared with predetermined desired output for confirmation of accuracy.

### GUI Testing
---

GUI testing was completed through rigorous manual testing. In addition to developer testing, a testing pool of 5 participants (all non-developers to simulate end-user interaction) were allowed to freely interact with the App. User experience and feedback for design, ease of use, and beginner-friendly instructions were positive. Upon being told to try to "break" the app through any means or input, none were successful.