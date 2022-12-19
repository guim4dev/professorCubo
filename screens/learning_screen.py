from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from components.green_button import GreenButton

class LearningScreen(Screen):
    def get_title_text(self, text, **kwargs):
        return Label(text=text, font_size=20, color=(0,0,0,1), bold=True, **kwargs)

    def get_subtitle_text(self, text, **kwargs):
        return Label(text=text, font_size=15, color=(0,0,0,1), italic=True, **kwargs)

    def get_content_text(self, text, **kwargs):
        return Label(text=text, font_size=10, color=(0,0,0,1), **kwargs)

    def get_header(self):
        header = GridLayout(rows=1, cols=2, size_hint=(1, None))
        goto_arcamera_button = GreenButton(text='Voltar', size_hint=(0.2, 0.1))
        goto_arcamera_button.bind(on_press=self.goto_arcamera)
        header.add_widget(goto_arcamera_button)
        header.add_widget(self.get_title_text(text="Como Resolver um Cubo Mágico", halign='left', valign='middle', size_hint=(0.8, 1)))
        return header

    def __init__(self, **kwargs):
        super(LearningScreen, self).__init__(**kwargs)
        self.scroll = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        self.layout = BoxLayout(orientation='vertical', size_hint=(1, None))
        self.layout.add_widget(self.get_header())
        self.scroll.add_widget(self.layout)
        self.add_widget(self.scroll)

    def goto_arcamera(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'arcamera'
