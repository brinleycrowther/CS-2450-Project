UVSim Command Line Guide
========================
UVSim is a simulator for executing BasicML programs, designed 
to help students learn machine language and computer architecture.

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
Which file would you like to run? 
Test1.txt

Enter word: +1234  # For READ at location 07
Enter word: +5678  # For READ at location 08
6912               # Output from WRITE at location 09
Program halted.

Key Features
- 100-word memory capacity (locations 00-99)
- Interactive input for READ operations
- Automatic memory display after execution
- Execution log with instruction details

File Requirements
1. .txt extension required.
2. One 4-digit word per line:
   - Instructions: Start with + followed by 4 digits (e.g., +1007)
   - Data: May use +/- (e.g., -5678)
3. Maximum 100 lines

Example Valid File:
+1007  # READ to 07
+1008  # READ to 08
+2007  # LOAD from 07
+3008  # ADD from 08
+2109  # STORE to 09
+1109  # WRITE from 09
+4300  # HALT

Troubleshooting
- "File does not exist in folder": Verify filename/path
- "Invalid word": Input must be 4 digits
- "File type invalid": Only .txt files accepted
- Program hangs: Include +4300 (HALT) instruction

Project Team
- Agustin Suarez Berios
- Brinley Crowther
- Owen Rasor
- Spencer Rohwer

Additional Documents
- Design specifications: uvsim-designDocument.docx
- Unit test spreadsheet: (see submitted files)
- Sprint meeting reports: (see submitted documents)
