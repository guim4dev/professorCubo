from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens.ar_screen import ARScreen
from kivy.logger import Logger, LOG_LEVELS
from screens.learning_screen import LearningScreen
from kivy.core.window import Window

Logger.setLevel(LOG_LEVELS["debug"])
class MainApp(App):
    def build(self):
        Window.clearcolor = (0.17, 0.14, 0.30, 1)
        screenManager = ScreenManager()
        self.screens = [ARScreen(name='arcamera'), LearningScreen(name='learning')]
        for screen in self.screens:
            screenManager.add_widget(screen)
        return screenManager

if __name__ == '__main__':
    app = MainApp(title='Professor Cubo')
    app.run()
