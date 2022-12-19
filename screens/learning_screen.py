from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from components.green_button import GreenButton
from yaml import load
from yaml import CLoader as Loader

class LearningScreen(Screen):
    def get_title_text(self, text, **kwargs):
        return Label(text=text, font_size='20sp', color=(0,0,0,1), bold=True, **kwargs)

    def get_subtitle_text(self, text, **kwargs):
        return Label(text=text, font_size='17sp', color=(0,0,0,1), italic=True, **kwargs)

    def get_content_text(self, text, **kwargs):
        return Label(text=text, font_size='13sp', color=(0,0,0,1), halign='left', **kwargs)

    def get_header(self):
        header = GridLayout(rows=1, cols=2, size_hint=(1, None))
        goto_arcamera_button = GreenButton(text='Voltar', size_hint=(0.2, None))
        goto_arcamera_button.bind(on_press=self.goto_arcamera)
        header.add_widget(goto_arcamera_button)
        header.add_widget(self.get_title_text(text=self.content_data['title'], halign='left', size_hint=(0.8, None)))
        return header

    def get_content(self):
        content = GridLayout(cols=1, size_hint=(1, None))
        for part in self.content_data['parts']:
            partContent = GridLayout(cols=1)
            partContent.add_widget(self.get_subtitle_text(text=f'Parte {part["number"]} - {part["title"]}'))
            for subpart in part['subparts']:
                subpartContent = GridLayout(cols=1)
                if subpart.get('title', False):
                    subpartContent.add_widget(self.get_subtitle_text(text=f'{part["number"]}.{subpart["number"]} - {subpart["title"]}'))
                if subpart.get('content', False):
                    subpartContent.add_widget(self.get_content_text(text=subpart['content']))
                partContent.add_widget(subpartContent)
            content.add_widget(partContent)
        return content

    def __init__(self, **kwargs):
        super(LearningScreen, self).__init__(**kwargs)
        with open('content/learning_screen.yml', 'r') as stream:
            self.content_data = load(stream, Loader) # load the content data from the yaml file

        # Setup layout
        self.layout = GridLayout(cols=1, spacing='10sp', size_hint_y=None, size_hint_x=1)
        self.layout.height = self.layout.minimum_height
        self.layout.add_widget(self.get_header())
        self.layout.add_widget(self.get_content_text(text=self.content_data['subtitle'], size_hint=(1, None)))
        self.layout.add_widget(self.get_content())
        
        # Setup Infinite Scroll
        self.scroll = ScrollView(size_hint=(1, None), do_scroll_y=True, do_scroll_x=False, size=(Window.width, Window.height))
        self.scroll.add_widget(self.layout)
        self.add_widget(self.scroll)

    def goto_arcamera(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'arcamera'
