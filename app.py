from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens.ar_screen import ARScreen
from screens.learning_screen import LearningScreen
from kivy.core.window import Window

class MainApp(App):
    def build(self):
        Window.clearcolor = (0.94, 0.97, 1, 1)
        screenManager = ScreenManager()
        screenManager.add_widget(ARScreen(name='arcamera'))
        screenManager.add_widget(LearningScreen(name='learning'))
        return screenManager

if __name__ == '__main__':
    app = MainApp(title='Professor Cubo')
    app.run()
