UVSim Command Line Guide
========================
UVSim is a simulator for executing BasicML programs, designed to help students learn machine language and computer architecture.

Prerequisites:
- Python 3.x installed on your system.

Installation:
1. Ensure Python 3.x is installed.
2. Download the UVSim files (`uvisim.py` and `accumulator.py`).

Usage:
1. Open a terminal/command prompt.
2. Navigate to the directory containing the UVSim files.
3. Run the simulator:
   python uvsim.py

Example Session
$ python uvsim.py
Which file would you like to run? Test1.txt

Enter word: 1234  # Input for first READ operation
Enter word: 5678  # Input for second READ operation
7902              # Program output from WRITE operation
Program halted.

Key Features
- Accepts BasicML files with 4-digit instructions
- Interactive input for READ operations
- Automatic memory display after execution
- Program log showing executed instructions

File Requirements
Input files must:
1. Have .txt extension
2. Contain one 4-digit instruction per line
3. Instructions must start with '+' (e.g., +1007) 
4. Data words may use +/- (e.g., -5678) 

Troubleshooting
- "File does not exist in folder": Verify correct path
- "Invalid word": Input must be 4 digits (e.g., 1234 or +5678)
- "File type invalid": Must use .txt files

Project Team
- Agustin Suarez Berios
- Brinley Crowther
- Owen Rasor
- Spencer Rohwer

Additional Documents
- Design specifications: uvsim-designDocument.docx
- Unit test spreadsheet: (see submitted files)
- Sprint meeting reports: (see submitted documents)
