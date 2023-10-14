from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen

# Builder.load_file('view/kv_files/leetcode_session_box_layout.kv')
Builder.load_file('view/kv_files/bots_box_layout.kv')
Builder.load_file('view/kv_files/app_header.kv')
Builder.load_file('view/kv_files/settings_layout.kv')

from view.py_files.bots_box_layout import LeetcodeBotsBoxLayout
# from view.py_files.leetcode_session_box_layout import LeetcodeSessionBoxLayout
from view.py_files.app_header import AppHeader
from view.py_files.settings_layout import SettingsScreenBoxLayout 

class MainWidget(BoxLayout):
  
  def switch_to_screen(self, next_screen):
    screen_manager = self.ids.screen_manager
    screen_manager.current = next_screen