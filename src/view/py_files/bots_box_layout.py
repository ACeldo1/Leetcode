import threading

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.animation import Animation

from kivy.graphics import Color, Rectangle, Ellipse

from backend.bot_scripts import generate_daily_challenge_markdown as GDC

class BotsScrollContentBoxLayout(BoxLayout):
  pass

class LeetcodeBotsBoxLayout(BoxLayout):
  def __init__(self, **kwargs):
    super(LeetcodeBotsBoxLayout, self).__init__(**kwargs)
    self.active_run_scripts = {}
    self.progressbar_animation = Animation(value=100, duration=2) + Animation(value=0, duration=0)
    self.progressbar_animation.repeat = True
  
  def daily_challenge_checkbox_callback(self, is_active, progressbar):
    if is_active:
      self.active_run_scripts[progressbar] = GDC
    else:
      del self.active_run_scripts[progressbar]
    
  def run_bot_scripts(self):
    print("Running selected scripts...")
    button = self.ids.run_checked_options_button
    button.disabled = True
    
    for progressbar in self.active_run_scripts.keys():
      progressbar.value = 0
      self.progressbar_animation.start(progressbar)
      
    threading.Thread(target=self.__execute_active_bot_options).start()
    button.disabled = False

  def __execute_active_bot_options(self):
    for progressbar, callback in self.active_run_scripts.items():
      callback()
      self.progressbar_animation.stop(progressbar)
      progressbar.value = 100

class LeetcodeBotsScrollView(ScrollView):
  pass

class DailyChallengeBoxLayout(BoxLayout):
  pass

class RunCheckedOptionsButton(Button):
  pass