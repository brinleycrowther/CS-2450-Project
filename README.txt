UVSim Command Line Guide
========================

Prerequisites:
- Python 3.6 or later (https://www.python.org/downloads/)

Installation:
1. Download or clone the repository:
   ```bash
   git clone https://github.com/your-team/uvsim.git

Navigate to the project directory:
- cd uvsim

Usage Instructions
1. Run the simulator:
python uvsim.py
2. When prompted, enter the path to your BasicML program file
3. Follow on-screen instructions for any required input

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
3. Example valid line: +1007 or 2007

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
