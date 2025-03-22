from kivy.uix.textinput import TextInput

class SimTextInput(TextInput):
    def __init__(self, text_key, **kwargs):
        super().__init__(**kwargs)
        self.text_key = text_key