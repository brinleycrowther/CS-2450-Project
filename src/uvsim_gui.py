# from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
# from threading import Thread
import os


class UVSimUI(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2

        from uvsim import UVSim # lazy import to avoid circular import, keeps logic and ui separate
        self.simulator = UVSim(self) # pass UI instance to UVSim

        self.left_half = self._left_half()
        self.right_half = self._right_half()
        self.add_widget(self.left_half)
        self.add_widget(self.right_half)

    # Left side layout
    def _left_half(self) -> BoxLayout:
        self.left_layout = BoxLayout(orientation='vertical', size_hint=(0.6, 1))

        # UVSim banner
        self.app_banner = Label(text="UVSim", size_hint_y=0.25, font_size=80, halign='left', valign='middle', padding=(50, 0))
        self.app_banner.bind(size=self.app_banner.setter('text_size'))
        self.left_layout.add_widget(self.app_banner)
        
        # File selection
        self.left_layout.add_widget(self._file_selection_layout())
        
        # Control buttons
        self.left_layout.add_widget(self._control_buttons())

        # Program Counter
        self.left_layout.add_widget(self._program_counter_layout())

        # Accumulator
        self.left_layout.add_widget(self._accumulator_layout())

        # Console Input
        self.left_layout.add_widget(self._console_input())

        # Console Output
        self.left_layout.add_widget(self._console_output_layout())

        ### Log button currently deprecated from design ###
        # self.left_layout.add_widget(self._log_button())

        return self.left_layout

    # File selection layout (File input, Select file button)
    def _file_selection_layout(self) -> BoxLayout:
        self.file_layout = BoxLayout(orientation='horizontal', size_hint_y=0.2, spacing=13, padding=(10, 5))
        self.file_layout.add_widget(Label(text="File:", size_hint_x=0.08))
        self.file_text_input = TextInput(text="", hint_text="Enter file name here, or select file:", multiline = False, size_hint=(0.5, 0.6), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.file_layout.add_widget(self.file_text_input)
        self.select_file_btn = Button(text="Select a File", size_hint_x=0.2)
        
        self.select_file_btn.bind(on_release = self._popup_file_chooser)
        self.file_text_input.bind(on_text_validate = self.file_handler)
        self.file_text_input.focus = True

        self.file_layout.add_widget(self.select_file_btn)
        return self.file_layout
    
    # File chooser popup
    def _popup_file_chooser(self, instance):
        self.popup_layout = BoxLayout(orientation='vertical')
        self.file_chooser = FileChooserIconView(show_hidden=False, path=os.getcwd())
        self.file_chooser.filters = ["*.txt"]
        self.file_chooser.bind(on_submit = self.file_chooser_handler)
        self.popup_layout.add_widget(self.file_chooser)

        self.popup_bttn_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10, padding=(10, 5))
        self.load_btn = Button(text="Load")
        self.cancel_btn = Button(text="Cancel")
        self.popup_bttn_layout.add_widget(self.load_btn)
        self.popup_bttn_layout.add_widget(self.cancel_btn)
        self.popup_layout.add_widget(self.popup_bttn_layout)

        self.popup = Popup(title="Select a File", content=self.popup_layout, size_hint=(0.9, 0.9))
        self.popup.open()
        self.load_btn.bind(on_release = self.file_chooser_handler)
        self.cancel_btn.bind(on_release = self.popup.dismiss)

    # File chooser load button on_release functionality
    def file_chooser_handler(self, instance=None, selection=None, touch=None):
        if len(self.file_chooser.selection) == 0:
            self.file_text_input.text = ""
        else:
            self.file_text_input.text = os.path.join(self.file_chooser.path, self.file_chooser.selection[0])
        self.popup.dismiss()
        self.file_handler(None)
    
    # File selection functionality (Enter key or File Chooser Load button)
    def file_handler(self, instance):
        selection = self.file_text_input.text
        if selection == "":
            self.simulator.update_console("No file selected. Please enter a valid file name.")
            return 0
        if not os.path.isabs(selection):
            selection = os.path.abspath(selection)
        
        file_try = self.simulator.fileInputToMemory(selection)
        self.file_text_input.text = ""
        if file_try == 0:
            self.refresh_memory_table(0)
            self.file_text_input.hint_text = "File loaded successfully!"
            self.file_text_input.disabled = True
            self.select_file_btn.disabled = True
            return 0
        else:
            return -1

    # Control buttons layout (Execute, Step, Stop, Save)
    def _control_buttons(self) -> BoxLayout:
        self.control_btn_layout = BoxLayout(orientation='horizontal', size_hint_y=0.2, spacing=10, padding=(10, 5))
        self.execute_btn = Button(text="Execute")
        self.step_btn = Button(text="Step")
        self.save_btn = Button(text="Save Memory")
        self.quit_btn = Button(text="Quit")
        
        self.control_btn_layout.add_widget(self.execute_btn)
        self.control_btn_layout.add_widget(self.step_btn)
        self.control_btn_layout.add_widget(self.save_btn)
        self.control_btn_layout.add_widget(self.quit_btn)

        self.execute_btn.bind(on_release = self.execute_handler)
        self.step_btn.bind(on_release = self.step_handler)
        self.save_btn.bind(on_release = self._popup_save_file)
        self.quit_btn.bind(on_release = self.quit_handler)

        return self.control_btn_layout
    
    # Save Popup for file saving location selection
    def _popup_save_file(self, instance):
        self.save_popup_layout = BoxLayout(orientation='vertical')
        self.save_file_chooser = FileChooserIconView(show_hidden=False, path=os.getcwd())
        self.save_popup_layout.add_widget(self.save_file_chooser)

        self.save_popup_filename_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10, padding=(10, 5))
        self.save_filename_input = TextInput(text="uvsim_save.txt", multiline=False, size_hint_y=0.7, pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.save_popup_filename_layout.add_widget(self.save_filename_input)
        self.save_btn = Button(text="Save", size_hint_x= 0.5)
        self.cancel_btn = Button(text="Cancel", size_hint_x=0.5)
        self.save_popup_filename_layout.add_widget(self.save_btn)
        self.save_popup_filename_layout.add_widget(self.cancel_btn)
        self.save_popup_layout.add_widget(self.save_popup_filename_layout)

        self.save_popup = Popup(title="Save File", content=self.save_popup_layout, size_hint=(0.9, 0.9))
        self.save_popup.open()
        self.save_btn.bind(on_release = self.save_file_handler)
        self.cancel_btn.bind(on_release = self.save_popup.dismiss)

    
    # Execute button's on_press functionality
    def execute_handler(self, instance):
        if self.file_text_input.disabled == True:
            self.simulator.wordProcess(False)
        else:
            self.simulator.update_console("No file loaded. Please load a file before executing.")
        return 0
    
    # Step button's on_press functionality
    def step_handler(self, instance):
        if self.file_text_input.disabled == True:
            self.simulator.wordProcess(True)
        else:
            self.simulator.update_console("No file loaded. Please load a file before stepping.")
        return 0
    
    # Save button's on_press functionality
    def save_file_handler(self, instance):
        if self.file_text_input.disabled == True:
            filename = self.save_filename_input.text.strip()
            if not filename.endswith(".txt"):
                filename += ".txt"
            directory = self.save_file_chooser.path
            if not os.path.isabs(directory):
                directory = os.path.abspath(directory)
            full_path = os.path.join(directory, filename)
            self.simulator.saveMemory(full_path)
            self.save_popup.dismiss()
        else:
            self.simulator.update_console("No file loaded. Please load and modify a file before saving.")
            self.save_popup.dismiss()
        return 0
    
    # Quit button's on_press functionality
    def quit_handler(self, instance):
        self.simulator.quit()

    # Program counter layout
    def _program_counter_layout(self) ->BoxLayout:
        self.pc_layout = BoxLayout(orientation='vertical', size_hint_y=0.25, spacing=0, padding=(20, 0))
        self.pc_label = Label(text="Program Counter:", size_hint_y=0.4, font_size=30, halign='left', valign='middle', padding=(40, 0))
        self.pc_label.bind(size=self.pc_label.setter('text_size'))
        self.pc_field = TextInput(text="Program Not Started", readonly=True, size_hint_y=0.4, padding=(20, 10))
        self.pc_layout.add_widget(self.pc_label)
        self.pc_layout.add_widget(self.pc_field)
        return self.pc_layout
    
    # Updates the program counter field
    def update_program_counter(self, value):
        self.pc_field.text = str(value)
        
    # Accumulator layout
    def _accumulator_layout(self) -> BoxLayout:
        self.accumulator_layout = BoxLayout(orientation='vertical', size_hint_y=0.25, spacing=0, padding=(20, 0))
        self.accumulator_label = Label(text="Accumulator:", size_hint_y=0.4, font_size=30, halign='left', valign='middle', padding=(40, 0))
        self.accumulator_label.bind(size=self.accumulator_label.setter('text_size'))
        self.accumulator_field = TextInput(text="No value in accumulator...", readonly=True, size_hint_y=0.4, padding=(20, 10))
        self.accumulator_layout.add_widget(self.accumulator_label)
        self.accumulator_layout.add_widget(self.accumulator_field)
        return self.accumulator_layout
    
    # adds current accumulator value to accumulator field
    def update_accumulator(self, value):
        self.accumulator_field.text = value
        
    # Console Input layout
    def _console_input(self) -> BoxLayout:
        self.console_in_layout = BoxLayout(orientation='vertical', size_hint_y=0.25, spacing=0, padding=(20, 0))
        self.console_label = Label(text="Console Input:", size_hint_y=0.4, font_size=30, halign='left', valign='middle', padding=(40, 0))
        self.console_label.bind(size=self.console_label.setter('text_size'))
        self.console_input = TextInput(multiline=False, size_hint_y=0.4, padding=(20, 10), disabled=True)
        self.console_input.bind(on_text_validate=self.input_text_handler)
        self.console_in_layout.add_widget(self.console_label)
        self.console_in_layout.add_widget(self.console_input)
        return self.console_in_layout
    
    # adds focus to console input text box
    def focus_console_input(self):
        self.console_input.disabled = False
        self.console_input.focus = True
    
    # handles the text input to pass to uvsim
    def input_text_handler(self, instance):
        input_word = instance.text
        instance.text = "" # clears text box
        instance.disabled = True

        self.simulator.process_input(input_word)
    
        return 0
    
    # Console Output layout
    def _console_output_layout(self) -> BoxLayout:
        self.console_out_layout = BoxLayout(orientation='vertical', spacing=10, padding=(20, 10))
        self.console_label = Label(text="Console Output:", size_hint_y=0.08, font_size=30, halign='left', valign='middle', padding=(40, 0))
        self.console_label.bind(size=self.console_label.setter('text_size'))
        self.console_scroller = ScrollView(bar_color=(0.2, 0.2, 0.2, 1), bar_width=10)
        self.console_output = TextInput(text="Welcome to UVSim!\nPlease load a file, then press Execute or Step to run.\n", multiline=True, readonly=True, size_hint=(1, None), padding=(10, 5))
        self.console_output.height = max( self.console_output.minimum_height, self.console_scroller.height * 4)
        self.console_scroller.add_widget(self.console_output)
        self.console_out_layout.add_widget(self.console_label)
        self.console_out_layout.add_widget(self.console_scroller)
        return self.console_out_layout
    
    # adds message to output console box
    def console_insert_text(self, message):
        self.console_output.text += f'{message}\n'

        # scroll to bottom to view latest message
        self.console_output.cursor = (0, len(self.console_output.text))
        
    ### Log button currently deprecated from design ###
    '''def _log_button(self) -> BoxLayout:
    #     self.log_layout = BoxLayout(orientation='horizontal', size_hint=(0.4, 0.2), spacing=10, padding=(50, 10))
    #     self.log_btn = Button(text="Display Log", size_hint_y=1)
    #     ### TODO finish button binding for on_press attribute ###
    #     self.log_layout.add_widget(self.log_btn)
    #     return self.log_layout'''

    # Right side layout (Memory Table)
    def _right_half(self):
        self.right_layout = BoxLayout(orientation='vertical', size_hint=(0.4, 1), padding=(10, 10))

        # Memory label
        self.memory_label = Label(text="Memory", size_hint_y=0.1, font_size=30, halign='left', valign='middle', padding=(50, 0))
        self.memory_label.bind(size=self.memory_label.setter('text_size'))
        self.right_layout.add_widget(self.memory_label)

        # Table header
        self.right_layout.add_widget(self._table_header())
        
        # Memory Table
        self.right_layout.add_widget(self._memory_table())
        
        return self.right_layout
    
    # Table header (Location, Word)
    def _table_header(self) -> GridLayout:
        self.table_header = GridLayout(cols=2, size_hint=(1, 0.15), spacing=2, padding=(15, 10))
        loc = Button(text="Location", disabled = True, background_color = (0.8, 0.8, 0.8, 1))
        loc.background_disabled_normal = ""
        loc.disabled_color = (0, 0, 0, 1)
        word = Button(text="Word", disabled = True, background_color = (0.8, 0.8, 0.8, 1))
        word.background_disabled_normal = ""
        word.disabled_color = (0, 0, 0, 1)
        self.table_header.add_widget(loc)
        self.table_header.add_widget(word)
        return self.table_header

    # Memory Table
    def _memory_table(self) -> ScrollView:
        self.memory_scroller = ScrollView(bar_color=(0.5, 0.5, 0.5, 1), bar_width=15, scroll_type=['bars', 'content'])
        self.memory_table = GridLayout(cols=2, spacing=2, padding=(15, 0), size_hint=(1, 8))

        self.refresh_memory_table()
        
        self.memory_scroller.add_widget(self.memory_table)
        
        return self.memory_scroller
    
    # Refresh Memory Table Function
    # NOTE: Memory table is made of disabled buttons, not labels. This is for color, grid, and design purposes.
    def refresh_memory_table(self, highlight_index = None):
        self.memory_table.clear_widgets()

        for key, value in self.simulator.memory.items():
            is_current = (highlight_index is not None and int(key) == highlight_index)
            loc = Button(text=str(key), disabled=True, background_color=(1, 1, 0.6, 0.7) if is_current else (0.8, 0.8, 0.8, 1))
            loc.disabled_color = (0, 0, 0, 1)
            loc.background_disabled_normal = ""
            word = Button(text=value, disabled=True, background_color=(1, 1, 0.6, 0.7) if is_current else (0.8, 0.8, 0.8, 1))
            word.disabled_color = (0, 0, 0, 1)
            word.background_disabled_normal = ""
            self.memory_table.add_widget(loc)
            self.memory_table.add_widget(word)
        return 0

    def make_reset_button(self):
        self.select_file_btn.disabled = False
        self.select_file_btn.text = "Reset App"
        self.select_file_btn.unbind(on_release = self.popup_file_chooser)
        self.select_file_btn.bind(on_release = self.reset_handler)
        return 0
    
    def reset_handler(self, instance):

        self.file_text_input.text = ""
        self.file_text_input.hint_text = "Enter file name here, or select file:"
        self.file_text_input.disabled = False

        self.select_file_btn.text = "Select a File"
        self.select_file_btn.unbind(on_release = self.reset_handler)
        self.select_file_btn.bind(on_release = self.popup_file_chooser)
        self.select_file_btn.disabled = False

        self.console_input.text = ""
        self.console_input.disabled = True

        self.console_output.text = "Welcome to UVSim!\nPlease load a file, then press Execute or Step to run.\n"
        self.console_output.cursor = (0, 0)

        self.accumulator_field.text = "No value in accumulator..."
        self.pc_field.text = "Program Not Started"
        self.simulator.reset()
        self.refresh_memory_table(0)

        return 0
    

"""class UVSimApp(App):
    def build(self):
        return UVSimUI()
    
def run_gui(uvsim_obj):
    global my_uvsim
    my_uvsim = uvsim_obj
    UVSimApp().run()
    return 0

if __name__ == "__main__":
    UVSimApp().run()"""
