from kivy.uix.button import Button

class GreenButton(Button):
    def __init__(self, **kwargs):
        super(GreenButton, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_color = [0.16, 0.66, 0.62, 1]
        self.background_down = ''
        self.color = (1, 1, 1, 1)