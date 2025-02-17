# from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from threading import Thread
import os


class UVSimUI(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        self.left_half = self._left_half()
        self.right_half = self._right_half()
        self.add_widget(self.left_half)
        self.add_widget(self.right_half)

        from uvsim import UVSim # lazy import to avoid cicular import, keeps logic and ui seperate
        self.simulator = UVSim(self) # pass UI instance to UVSim

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

        # Accumulator
        self.left_layout.add_widget(self._accumulator_layout())

        # Console Input
        self.left_layout.add_widget(self._console_input())

        # Console Output
        self.left_layout.add_widget(self._console_output_layout())

        # Log button
        self.left_layout.add_widget(self._log_button())

        return self.left_layout

    # File selection layout (File input, Select file button)
    def _file_selection_layout(self) -> BoxLayout:
        self.file_layout = BoxLayout(orientation='horizontal', size_hint_y=0.2, spacing=13, padding=(10, 5))
        self.file_layout.add_widget(Label(text="File:", size_hint_x=0.08))
        self.file_text_input = TextInput(hint_text="Enter file name here", multiline = False, size_hint=(0.5, 0.6), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.file_layout.add_widget(self.file_text_input)
        self.select_file_btn = Button(text="Select File", size_hint_x=0.2)
        
        self.select_file_btn.bind(on_press = self.file_handler)

        self.file_layout.add_widget(self.select_file_btn)
        return self.file_layout
    
    def file_handler(self, instance):
        selection = self.file_text_input.text
        if not os.path.isabs(selection):
            selection = os.path.abspath(selection)
        
        self.simulator.fileInputToMemory(selection)

    # Control buttons layout (Execute, Step, Stop, Save)
    def _control_buttons(self) -> BoxLayout:
        self.control_btn_layout = BoxLayout(orientation='horizontal', size_hint_y=0.2, spacing=10, padding=(10, 5))
        self.execute_btn = Button(text="Execute")
        self.step_btn = Button(text="Step")
        self.stop_btn = Button(text="Stop")
        self.save_btn = Button(text="Save")
        ### TODO finish button bindings for on_press attributes ###
        self.control_btn_layout.add_widget(self.execute_btn)
        self.control_btn_layout.add_widget(self.step_btn)
        self.control_btn_layout.add_widget(self.stop_btn)
        self.control_btn_layout.add_widget(self.save_btn)

        self.execute_btn.bind(on_press = lambda instance: self.simulator.wordProcess(False))
        self.step_btn.bind(on_press = lambda instance: self.simulator.wordProcess(True))

        return self.control_btn_layout
        
    # Accumulator
    def _accumulator_layout(self) -> BoxLayout:
        self.accumulator_layout = BoxLayout(orientation='vertical', size_hint_y=0.25, spacing=0, padding=(20, 0))
        self.accumulator_label = Label(text="Accumulator:", size_hint_y=0.4, font_size=30, halign='left', valign='middle', padding=(40, 0))
        self.accumulator_label.bind(size=self.accumulator_label.setter('text_size'))
        self.accumulator_field = TextInput(text="No value in accumulator...", readonly=True, size_hint_y=0.4)
        self.accumulator_layout.add_widget(self.accumulator_label)
        self.accumulator_layout.add_widget(self.accumulator_field)
        return self.accumulator_layout
    
    # adds current accumulator value to accumulator field
    def update_accumulator(self, value):
        self.accumulator_field.text = value
        
    # Console Input
    def _console_input(self) -> BoxLayout:
        self.console_in_layout = BoxLayout(orientation='vertical', size_hint_y=0.25, spacing=0, padding=(20, 0))
        self.console_label = Label(text="Console Input:", size_hint_y=0.4, font_size=30, halign='left', valign='middle', padding=(40, 0))
        self.console_label.bind(size=self.console_label.setter('text_size'))
        self.console_input = TextInput(multiline=False, size_hint_y=0.4)
        ### TODO create button or enter key binding for console input ###
        self.console_input.bind(on_text_validate=self.input_text_handler)
        self.console_in_layout.add_widget(self.console_label)
        self.console_in_layout.add_widget(self.console_input)
        return self.console_in_layout
    
    # handles the text input to pass to uvsim
    def input_text_handler(self, instance):
        input_word = instance.text

        self.simulator.process_input(input_word)
        
        instance.text = "" # clears text box
    
    # Console Output
    def _console_output_layout(self) -> BoxLayout:
        self.console_out_layout = BoxLayout(orientation='vertical', spacing=10, padding=(20, 10))
        self.console_label = Label(text="Console Output:", size_hint_y=0.08, font_size=30, halign='left', valign='middle', padding=(40, 0))
        self.console_label.bind(size=self.console_label.setter('text_size'))
        self.console_scroller = ScrollView(bar_color=(0.2, 0.2, 0.2, 1), bar_width=10)
        self.console_output = TextInput(text="", multiline=True, readonly=True, size_hint=(1, None))
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
        
        # Log button
    def _log_button(self) -> BoxLayout:
        self.log_layout = BoxLayout(orientation='horizontal', size_hint=(0.4, 0.2), spacing=10, padding=(50, 10))
        self.log_btn = Button(text="Display Log", size_hint_y=1)
        ### TODO finish button binding for on_press attribute ###
        self.log_layout.add_widget(self.log_btn)
        return self.log_layout

    # Right side layout (Memory Table
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
    
    # Table header
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
        self.memory_table = GridLayout(cols=2, spacing=2, padding=(15, 0), size_hint=(1, 10))

        if "my_uvsim" in globals():
            self.refresh_memory_table()
        else:
            for i in range(100):
                loc = Button(text=f"Loc {i}", disabled=True, background_color=(0.8, 0.8, 0.8, 1))
                loc.disabled_color = (0, 0, 0, 1)
                loc.background_disabled_normal = ""
                word = Button(text=f"Word {i}", disabled = True, background_color = (0.8, 0.8, 0.8, 1))
                word.background_disabled_normal = ""
                word.disabled_color = (0, 0, 0, 1)
                self.memory_table.add_widget(loc)
                self.memory_table.add_widget(word)
        self.memory_scroller.add_widget(self.memory_table)
        
        return self.memory_scroller
    
    # Refresh Memory Table Function
    def refresh_memory_table(self):
        self.memory_table.clear_widgets()
        for key, value in self.simulator.memory.items():
            loc = Button(text=str(key), disabled=True, background_color=(0.8, 0.8, 0.8, 1))
            loc.disabled_color = (0, 0, 0, 1)
            loc.background_disabled_normal = ""
            word = Button(text=value, disabled=True, background_color=(0.8, 0.8, 0.8, 1))
            word.disabled_color = (0, 0, 0, 1)
            word.background_disabled_normal = ""
            self.memory_table.add_widget(loc)
            self.memory_table.add_widget(word)
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
