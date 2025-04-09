import json
from pathlib import Path
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class ColorScheme:
    DEFAULT_COLORS = {
        "primary": "#4C721D",  # UVU Dark Green
        "secondary": "#FFFFFF",  # White
        "text": "#000000"  # Black
    }

    def __init__(self):
        self.config_path = Path(App.get_running_app().user_data_dir) / "color_scheme.json"
        self.colors = self.DEFAULT_COLORS.copy()
        self.load()

    def load(self):
        self.colors = self.DEFAULT_COLORS.copy()
        self.save()

    def save(self):
        with open(self.config_path, 'w') as f:
            json.dump(self.colors, f)

    def update(self, primary, secondary, text="#000000"):
        self.colors.update({
            "primary": primary,
            "secondary": secondary,
            "text": text
        })
        self.save()


class ColorConfigPopup(Popup):
    def __init__(self, color_scheme, callback, **kwargs):
        super().__init__(**kwargs)
        self.title = "Color Configuration"
        self.size_hint = (0.8, 0.6)
        self.color_scheme = color_scheme
        self.callback = callback

        layout = GridLayout(cols=2, padding=10, spacing=10)
        
        layout.add_widget(Label(text="Primary Color (Hex):"))
        self.primary_input = TextInput(text=color_scheme.colors["primary"])
        layout.add_widget(self.primary_input)

        layout.add_widget(Label(text="Secondary Color (Hex):"))
        self.secondary_input = TextInput(text=color_scheme.colors["secondary"])
        layout.add_widget(self.secondary_input)

        buttons = BoxLayout(size_hint_y=0.2, spacing=10)
        buttons.add_widget(Button(text="Apply", on_press=self.apply))
        buttons.add_widget(Button(text="Cancel", on_press=self.dismiss))
        
        layout.add_widget(buttons)
        self.add_widget(layout)

    def apply(self, instance):
        primary = self.primary_input.text.strip()
        secondary = self.secondary_input.text.strip()
        
        if len(primary) != 7 or len(secondary) != 7:
            return
            
        self.color_scheme.update(primary, secondary)
        self.callback()
        self.dismiss()