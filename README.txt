UVSim - Basic Machine Language Simulator
========================================

Description:
UVSim is a virtual machine simulator for executing BasicML programs. It was designed for computer science education and emulates a 100-word memory architecture with CPU operations including I/O, arithmetic, and control flow.

Installation:
1. Install: 
   Python 3.6+
2. Clone repository:
   git clone https://github.com/your-team/uvsim.git
3. Navigate to project:
   cd uvsim

Usage:
1. Run simulator with:
   python uvsim.py
2. When prompted, enter path to BasicML file (e.g., "Test1.txt")

Sample Input Files:
- Test1.txt: Basic program with READ/LOAD/ADD/WRITE/HALT
- Test2.txt: Program demonstrating branching and subtraction

Input Format:
- One 4-digit signed decimal instruction per line
- Example:
  +1007
  +2007
  +4300

Supported Operations:
| Opcode | Mnemonic    | Description                   |
|--------|-------------|-------------------------------|
| 10     | READ        | Input to memory location      |
| 11     | WRITE       | Output from memory location   |
| 20     | LOAD        | Mem -> Accumulator            |
| 21     | STORE       | Accumulator -> Mem            |
| 30     | ADD         | Accumulator += Mem            |
| 31     | SUBTRACT    | Accumulator -= Mem            |
| 32     | DIVIDE      | Accumulator /= Mem            |
| 33     | MULTIPLY    | Accumulator *= Mem            |
| 40     | BRANCH      | Unconditional jump            |
| 41     | BRANCHNEG   | Jump if Accumulator < 0       |
| 42     | BRANCHZERO  | Jump if Accumulator == 0      |
| 43     | HALT        | Stop program execution        |

Example Session:
$ python uvsim.py
Enter BasicML file path: Test1.txt
READ operation - Enter a number: 5
WRITE operation - Output: 15
Program halted successfully

Project Files:
- uvsim.py                  : Main simulator logic
- accumulator.py            : Accumulator component
- test_*.py                 : Unit tests
- *.txt                     : Sample programs
- uvsim-designDocument.docx : Design specs

Limitations:
- 100-word memory limit
- No floating-point support

Contributors:
- Agustin Suarez Berios
- Brinley Crowther 
- Owen Rasor
- Spencer Rohwer
