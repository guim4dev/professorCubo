from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.camera import Camera
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.logger import Logger
import cv2
from explore import run_cube_solver
from components.green_button import GreenButton 

class ARScreen(Screen):
    def __init__(self, **kwargs):
        super(ARScreen, self).__init__(**kwargs)
        self.layout = FloatLayout()
        
        goto_learning_button = GreenButton(text='Aprenda!', size_hint=(.2, .1), pos_hint={'x': .79, 'y': .01})
        goto_learning_button.bind(on_press=self.goto_learning)
        self.layout.add_widget(goto_learning_button)
        Logger.debug('carregando imagem')
        self.opencv2_cam = Image()
        Logger.debug('captura')
        self.capture = cv2.VideoCapture(1)
        Logger.debug('captura depois')

        Logger.debug('set clock')
        Clock.schedule_interval(self.update, 1.0/20.0)
        
        Logger.debug('add layout')
        
        self.layout.add_widget(self.opencv2_cam)
        self.add_widget(self.layout)

        Logger.debug('add widget')

    def update(self, dt):
        Logger.debug('updateeeeeeeeee')
        _, frame = self.capture.read() 
        Logger.debug('read capturado')
        run_cube_solver(frame) # Solve cube and add it to captured frame
        Logger.debug('solucionado')
        Logger.debug('mostrou o frame')
        
        # convert it to texture
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr') 
        #if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer. 
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        Logger.debug('convertido')
        # display image from the texture
        self.opencv2_cam.texture = texture
        Logger.debug('setado')

    def goto_learning(self, *args):
        self.manager.transition.direction = 'left'
        self.manager.current = 'learning'
    
    def destroy(self):
        self.capture.release()
        cv2.destroyAllWindows()