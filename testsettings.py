from kivy.app import App
from kivy.uix.button import Button


class SettingsApp(App):
    def build(self):
        return Button(on_press=self.open_settings, text='Press me')


SettingsApp().run()