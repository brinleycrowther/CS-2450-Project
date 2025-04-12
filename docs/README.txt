UVSim Command Line Guide
========================
UVSim is a simulator for executing BasicML programs, designed 
to help students learn machine language and computer architecture.

Prerequisites:
- Python 3.x installed on your system.

Installation:
1. Ensure Python 3.x is installed.
2. Install required dependencies:
   pip install kivy
3. Download all src files (uvsim.py, accumulator.py, uvsim_gui.py, simtextinput.py, color_scheme.py, __init__.py)

Running the GUI:
1. Navigate to the directory containing the files
2. Run the simulator:
   python uvsim.py

GUI Usage Guide:
1. Load a Program:
- Type file path in "File:" text box and press Enter
  OR
- Click "Select A File" to choose a file from a file picker
- Modify values directly in the memory table (Can use Cut/Copy/Paste)
- Supported files: .txt with BasicML code (4 or 6 digit words)
- Invalid inputs are automatically rejected
2. Execute Program:
- Execute Button: Run entire program
- Step Button: Execute one instruction at a time
- Program counter shown in memory table
3. Console Interaction:
- During READ operations:
   1. Console Input field becomes active
   2. Enter 6-digit values (+/-123456 format)
   3. Press Enter to submit
4. Memory Display:
- Right panel shows memory contents
- Updated in real-time during execution
- Locations 00-249 shown as [Location][Word] pairs
- Words can be modified in the table (copy/paste function)
5. Program Controls:
- Save Button: Save current state to specified directory as default uvsim_save.txt
- Quit Button: Exit application
- Accumulator value displayed below controls
- Reset App Button: Resets program for additional use (Available once a file has run to completion).
- Settings: Set the app color scheme
- Edit File: Change words from input file
6. Run Another Program:
- Select "New Tab+"
- Switch between files by selecting the black tabs box for drop down menu
- Run program as directed above

Example GUI Session:
1. Launch application
2. Enter "test_program.txt" in File field
3. Click "Select A File"
4. Click "Step" to execute instructions one-by-one
5. When READ operation occurs:
   - Type input value in Console Input
   - Press Enter to continue
6. View results in Console Output.
7. Click "Save" to export state when finished
8. Click Reset App to run program again.
9. Click Quit to exit.
	- OR -
8. Click "Edit File".
9. Make edits to words and click "Save".
10. Click "Execute".
11. Click "Quit" to exit.

Key Features:
- Graphical memory table with real-time updates
- Customizable color schemes via config file
- Step-through execution for debugging
- Integrated console for input/output
- Visual accumulator status display
- User-defined save locations
- Responsive UI with clear error messages

File Requirements
1. .txt extension required.
2. One 6-digit word per line:
   - Instructions: Start with + followed by 6 digits (e.g., +001007)
   - Data: May use +/- (e.g., -005678)
3. Maximum 250 lines

Example Valid File:
+010007  & +100007 # READ to 07
+010008  & +100008 # READ to 08
+020007  & +200007 # LOAD from 07
+030008  & +300008 # ADD from 08
+021009 & +210009 # STORE to 09
+011009  & +110009 # WRITE from 09
+043000  & +430000 # HALT

Troubleshooting
- Blank window: Verify Kivy installation
- Input not working: Check active field (colored border indicates focus)
- Missing buttons: Resize window to ensure proper layout
- Font rendering issues: Update graphics drivers
- File loading failures: Use absolute paths (e.g., C:/path/to/file.txt)

Project Team
- Agustin Suarez Berios
- Brinley Crowther
- Owen Rasor
- Spencer Rohwer

Additional Documents
- Design specifications: uvsim-designDocument.docx
- Unit test spreadsheet: (see submitted files)
- Sprint meeting reports: (see submitted documents)
