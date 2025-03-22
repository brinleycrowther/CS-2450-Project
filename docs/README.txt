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
3. Download all project files (uvsim.py, accumulator.py, uvsim_gui.py)

Running the GUI:
1. Navigate to the directory containing the files
2. Run the simulator:
   python uvsim.py

GUI Usage Guide:
1. Load a Program:
- Type file path in "File:" text box and press Enter
  OR
- Click "Select File" to choose a file from a file picker
- Supported files: .txt with BasicML code
2. Execute Program:
- Execute Button: Run program continuously
- Step Button: Execute one instruction at a time
- Program counter shown in memory table
3. Console Interaction:
- During READ operations:
   1. Console Input field becomes active
   2. Enter 4-digit values (+/-1234 format)
   3. Press Enter to submit
4. Memory Display:
- Right panel shows memory contents
- Updated in real-time during execution
- Locations 00-99 shown as [Location][Word] pairs
5. Program Controls:
- Save Button: Save current state to specified directory as default UVSim_output.txt
- Quit Button: Exit application
- Accumulator value displayed below controls
- Reset App Button: Available once a file has run to completion. Resets program for additional use.

Example GUI Session:
1. Launch application
2. Enter "test_program.txt" in File field
3. Click "Select File"
4. Click "Step" to execute instructions one-by-one
5. When READ operation occurs:
   - Type input value in Console Input
   - Press Enter to continue
6. View results in Console Output
7. Click "Save" to export state when finished
8. Click Reset App to run program again.
9. Click Quit to exit.

Key Features:
- Graphical memory table with real-time updates
- Step-through execution for debugging
- Integrated console for input/output
- Visual accumulator status display
- One-click state saving
- Responsive UI with clear error messages

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
- Blank window: Verify Kivy installation
- Input not working: Check active field (green border indicates focus)
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
