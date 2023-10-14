from kivy.core.window import Window
from kivy.app import App
from kivy.lang import Builder

# load main widget file
Builder.load_file('view/kv_files/main_widget.kv')

from view.py_files.main_widget import MainWidget
from backend.bot_scripts import generate_daily_challenge_markdown

Window.minimum_width, Window.minimum_height = 600, 475

class MainApp(App):
  def build(self):
    return MainWidget()

if __name__ == '__main__':
  MainApp().run()