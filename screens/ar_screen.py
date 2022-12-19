from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from components.green_button import GreenButton 

class ARScreen(Screen):
    def __init__(self, **kwargs):
        super(ARScreen, self).__init__(**kwargs)
        self.layout = FloatLayout()
        goto_learning_button = GreenButton(text='Aprenda!', size_hint=(.2, .1), pos_hint={'x': .79, 'y': .01})
        goto_learning_button.bind(on_press=self.goto_learning)
        self.layout.add_widget(goto_learning_button)
        self.add_widget(self.layout)

    def goto_learning(self, *args):
        self.manager.transition.direction = 'left'
        self.manager.current = 'learning'