from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder

Builder.load_file('view/kv_files/leetcode_session_box_layout.kv')

from view.py_files.leetcode_session_box_layout import LeetcodeSessionBoxLayout
class SettingsScreenBoxLayout(BoxLayout):
  pass

class ConfigSettingsScrollView(ScrollView):
  pass

class ConfigSettingsBoxLayout(BoxLayout):
  pass

class LeetcodeUsernameBoxLayout(BoxLayout):
  pass

class LeetcodePasswordBoxLayout(BoxLayout):
  pass

class LeetcodeLanguageBoxLayout(BoxLayout):
  pass