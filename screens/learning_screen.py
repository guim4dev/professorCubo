from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.videoplayer import VideoPlayer
from kivy.core.window import Window
from components.green_button import GreenButton
from yaml import load
from yaml import CLoader as Loader

class LearningScreen(Screen):
    def get_title_text(self, text, **kwargs):
        return Label(text=text, font_size='20sp', color=(1,1,1,1), bold=True, **kwargs)

    def get_header(self):
        header = GridLayout(rows=1, cols=2, size_hint=(1, None))
        goto_arcamera_button = GreenButton(text='Voltar', size_hint=(0.2, None))
        goto_arcamera_button.bind(on_press=self.goto_arcamera)
        header.add_widget(goto_arcamera_button)
        header.add_widget(self.get_title_text(text=self.content_data['title'], halign='left', size_hint=(0.8, None)))
        return header

    def get_video_player(self):
        player = VideoPlayer(source="content/cubeVideo.mp4", options={'allow_stretch': True})
        player.thumbnail = 'content/cubeVideoThumbnail.jpg'
        return player

    def __init__(self, **kwargs):
        super(LearningScreen, self).__init__(**kwargs)
        with open('content/learning_screen.yml', 'r') as stream:
            self.content_data = load(stream, Loader) # load the content data from the yaml file

        # Setup layout
        self.layout = BoxLayout(orientation='vertical', size_hint_y=None, size_hint_x=1, height=Window.height)
        self.layout.add_widget(self.get_header())
        self.video_player = self.get_video_player()
        self.layout.add_widget(self.video_player)
        self.add_widget(self.layout)

    def goto_arcamera(self, *args):
        self.video_player.state = 'pause'
        self.manager.transition.direction = 'right'
        self.manager.current = 'arcamera'

    def destroy(self):
        print("DESTROY LEARNING SCREEN")
