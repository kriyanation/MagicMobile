import os
import random
from threading import Thread

from kivy.animation import Animation
from kivy.app import App
from kivy.core.clipboard import Clipboard
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

from kivy.clock import  Clock
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from plyer import tts
from kivy.core.window import Window
#Window.clearcolor = (1, 1, 1, 1)
import data_capture_lessons
import data_lessons
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,disable_multitouch')


NUMBER_OF_STEPS = 7


class LessonListScreen(Screen):
    container = ObjectProperty(None)
    def __init__(self,**kwargs):
        super(LessonListScreen, self).__init__(**kwargs)

        print("Hello")
        Clock.schedule_once(self.add_buttons,1)

    def add_buttons(self,dt):
        self.list_lessons = data_capture_lessons.get_Lessons()
        self.container.bind(minimum_height=self.container.setter('height'))
        for element in self.list_lessons:
            button = Button(text=element[1],background_color=[0.76,0.83,0.86,0.8],pos_hint={'x': .15,'top': 1},size_hint_y=None,size_hint_x=0.7)
            button.on_release = lambda instance=button, a=element[0]: self.switch_to_title(instance, a)
            self.container.add_widget(button)

    def switch_to_title(self,i,a):
        self.selected_lesson = a
        self.manager.current ="title"
    def launch_popup(self):
        show = ImportPop()
        self.popupWindow = Popup(title="Import Lesson", content=show,
                            size_hint=(1, 0.7),auto_dismiss=False)
        show.set_popupw(self.popupWindow)
        show.set_screen_instance(self)
        # open popup window
        self.popupWindow.open()






class ImportPop(BoxLayout):
    text_userid = StringProperty()
    text_classid = StringProperty()
    text_lessonid = StringProperty()
    text_status = StringProperty()

    def __init__(self, **kwargs):

        super(ImportPop, self).__init__(**kwargs)

    def import_lesson(self):

        self.text_status = "Accessing the Lesson....."

        print(self.text_classid+self.text_userid+self.text_lessonid)
        response_code = data_lessons.import_new_lesson(self.text_userid,self.text_classid,self.text_lessonid)
        if response_code == 1:
            self.text_status = "There was an error accessing the lesson. Check your access details."
        else:
            self.text_status = "Access details correct. Importing the lesson..."
            for child in self.listscreen.container.children:
                self.listscreen.container.remove_widget(child)
            self.listscreen.add_buttons(1)
            self.popw.dismiss()

    def close_pop(self):
        self.popw.dismiss()

    def set_popupw(self,pop):
        self.popw=pop

    def set_screen_instance(self,listscreen):
        self.listscreen =listscreen





class LessonTitleScreen(Screen):
    text_label_1 = StringProperty()
    text_label_2 = StringProperty()
    text_image= StringProperty()

    def __init__(self,**kwargs):
        super(LessonTitleScreen,self).__init__(**kwargs)
    def read_intro(self):
        tts.speak(self.text_label_1)
    def on_enter(self):
        lessonid = self.manager.get_screen('lessons').selected_lesson
        title, title_image, title_running_notes = data_capture_lessons.get_title_info(lessonid)
        self.text_label_1 = title_running_notes
        self.text_label_2 = title
        imagepath = "Lessons/Lesson"+str(lessonid)+"/images/"+title_image
        if os.path.exists(imagepath):
            self.text_image = imagepath
        else:
            self.text_image = "placeholder.png"



    def set_previous_screen(self):
        if self.manager.current == 'title':
            self.manager.transition.direction = 'right'
            self.manager.current = self.manager.previous()
    def set_next_screen(self):
        if self.manager.current == 'title':
            self.manager.transition.direction = 'left'
            self.manager.current = self.manager.next()

class LessonFactualScreen(Screen):


    text_image_1 = StringProperty()
    text_image_2 = StringProperty()
    text_image_3 = StringProperty()
    text_term_description_1 = StringProperty()
    text_term_description_2  = StringProperty()
    text_term_description_3  = StringProperty()

    def on_enter(self):
        lessonid = self.manager.get_screen('lessons').selected_lesson
        textimage_1, textimage_2, textimage_3 = data_capture_lessons.get_fact_images(lessonid)
        text_term_1, text_term_2, text_term_3 = data_capture_lessons.get_fact_terms(lessonid)
        textterm_description_1,textterm_description_2 ,textterm_description_3 = data_capture_lessons.get_fact_descriptions(lessonid)
        imagepath = "Lessons/Lesson" + str(lessonid) + "/images/"

        self.text_image_1 =  imagepath+textimage_1
        self.text_image_2 = imagepath + textimage_2
        self.text_image_3 = imagepath + textimage_3

        self.text_term_description_1 = text_term_1+" : "+textterm_description_1
        self.text_term_description_2 = text_term_2 + " : " + textterm_description_2
        self.text_term_description_3 = text_term_3 + " : " + textterm_description_3

        if not os.path.exists( self.text_image_1 ):
            self.text_image_1 = "placeholder.png"
        if not os.path.exists(self.text_image_2):
            self.text_image_2 = "placeholder.png"
        if not os.path.exists(self.text_image_3):
            self.text_image_3 = "placeholder.png"
    def read_aloud(self):
        tts.speak(self.text_to_read)

    def set_previous_screen(self):
        if self.manager.current == 'factual':
            self.manager.transition.direction = 'right'
            self.manager.current = self.manager.previous()
    def set_next_screen(self):
        if self.manager.current == 'factual':
            self.manager.transition.direction = 'left'
            self.manager.current = self.manager.next()
    def slide_moved(self):
        print(str(self.car.index))
        if self.car.index == 0:
            self.text_to_read = self.text_term_description_1
        elif self.car.index == 1:
            self.text_to_read = self.text_term_description_2
        else:
            self.text_to_read = self.text_term_description_3

class LessonApplyScreen(Screen):
    text_label_1 = StringProperty("Dynamic Text"+str(random.randint(1,100)))
    text_label_2 = StringProperty("test.png")
    steps = ObjectProperty(None)
    def __init__(self,**kwargs):
        super(LessonApplyScreen, self).__init__(**kwargs)
        self.anim = Animation(size=(200, 200), t='in_quad')




    def on_enter(self):

        self.lessonid = self.manager.get_screen('lessons').selected_lesson
        self.number_of_steps = data_capture_lessons.get_number_of_steps(self.lessonid)
        self.step_list = data_capture_lessons.get_description_list(self.lessonid)
        self.image_list = data_capture_lessons.get_step_image_list(self.lessonid)
        self.add_steps_buttons()

    def set_previous_screen(self):
        if self.manager.current == 'apply':
            self.manager.transition.direction = 'right'
            self.manager.current = self.manager.previous()
    def set_next_screen(self):
        if self.manager.current == 'apply':
            self.manager.transition.direction = 'left'
            self.manager.current = self.manager.next()

    def add_steps_buttons(self):
       # self.steps.bind(minimum_height=self.steps.setter('height'))
        self.button_list = []
        self.steps.clear_widgets()
        self.images.clear_widgets()
        # ss = self.steps.children
        # for child in ss:
        #     self.steps.remove_widget(child)
        # for child in self.images.children:
        #     self.steps.remove_widget(child)


        for i in range(self.number_of_steps):
            button = Button(text=self.step_list[i], size_hint_y=None,size_hint_x=1
                            ,background_color=[0.76,0.83,0.86,0.8],text_size=(200, None))
            if i != 0:
                button.disabled = True
            self.button_list.append(button)
            button.on_release = lambda instance=button,a =i: self.add_image(instance,a)
            self.steps.add_widget(button)


    def add_image(self,instance,a,*args):
        print(a)
        print(instance)
        instance.disabled = True
        if a < self.number_of_steps-1:
            button = self.button_list[a+1]
            button.disabled = False
        imagepath = "Lessons/Lesson" + str(self.lessonid) + "/images/"
        image = Image(source=imagepath+self.image_list[a],size=(50,50),size_hint_y=None)
        self.images.add_widget(image)
        self.anim.start(image)
        sound_thread = Thread(target=tts.speak, args=(self.step_list[a],))
        sound_thread.start()

class LessonAssessScreen(Screen):
        text_label_1 = StringProperty()
        text_label_2 = StringProperty()
        steps = ObjectProperty(None)

        def __init__(self, **kwargs):
            super(LessonAssessScreen, self).__init__(**kwargs)

        def on_enter(self):
            self.lessonid = self.manager.get_screen('lessons').selected_lesson
            self.text_label_1, self.text_label_2 = data_capture_lessons.get_questions_answer(self.lessonid)

        def on_save(self):
            ret = data_capture_lessons.set_answer(self.lessonid,self.text_label_2)
            print(self.text_label_2)
            print(str(ret))
        def on_share(self):
            Clipboard.copy(self.text_label_2)


        def set_next_screen(self):
            if self.manager.current == 'assess':
                self.manager.transition.direction = 'left'
                self.manager.current = 'lessons'



class Popups(BoxLayout):
    pass
class ScreenManagement(ScreenManager):
    pass
class MagicRoomApp(App):

    def build(self):

        return ScreenManagement()


MagicRoomApp().run()

