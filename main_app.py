# программа с двумя экранами
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from instructions import *
from ruffier import test
from seconds import *
from kivy.core.window import Window
from kivy.animation import Animation
from runner import *
from sits import *
# Экран (объект класса Screen) - это виджет типа "макет" (Screen - наследник класса RelativeLayout).
# ScreenManager - это особый виджет, который делает видимым один из прописанных в нём экранов.
# class MainScr(Screen):
#     def __init__(self,name ='main'):
#         super().
pink = (0.87, 0.54, 0.8, 1)
yellow = (1,0.8,0,1)
skyblue = (.5,.7,1,1)

Window.clearcolor = skyblue

age, name, p1, p2, p3 = 0, '', 0, 0, 0

def check_int(str_num):
    try:
        return int(str_num)
    except:
        return False

class FirstScr(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        Vlayout = BoxLayout(orientation='vertical')
        insrt_lbl = Label(text=txt_instruction)
        Hlayout1 = BoxLayout(size_hint=(.8,None),height = '30sp')
        name_lbl = Label(text='[color=#000080]' + 'Введите имя:' + '[/color]', markup = True)
        age_lbl = Label(text='Введите возраст:')
        self.name_input = TextInput(multiline = False)
        self.age_input = TextInput(multiline = False)
        
        Vlayout.add_widget(insrt_lbl)

        Hlayout2 = BoxLayout(size_hint=(.8,None),height = '30sp')
        btn_color = (0,0,.8,1)
        btn_ok = Button(text='Начать',size_hint=(.3,.2),pos_hint={'center_x':0.5})
        btn_ok.background_color = btn_color
        btn_ok.on_press = self.next
        
        Hlayout1.add_widget(name_lbl)
        Hlayout2.add_widget(age_lbl)
        Hlayout1.add_widget(self.name_input)
        Hlayout2.add_widget(self.age_input)
        Vlayout.add_widget(Hlayout1)
        Vlayout.add_widget(Hlayout2)
        Vlayout.add_widget(btn_ok)
        

        self.add_widget(Vlayout)

    def next(self):
        global age, name
        name = self.name_input.text
        age = self.age_input.text
        age = check_int(age)
        if age == False or age < 7:
            age = 7
            self.age_input.text = str(age)
        else:
            self.manager.current='second'
        
        
class SecondScr(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.next_screen = False
        Vlayout = BoxLayout(orientation = 'vertical')
        lbl1 = Label(text = txt_test1)
        
        Vlayout.add_widget(lbl1)

        Hlayout1 = BoxLayout(size_hint=(.8,None),height = '30sp')
        input_lbl = Label(text='Введите результат:')
        Hlayout1.add_widget(input_lbl)
        self.sec = Seconds(2)
        self.sec.bind(done = self.sec_finished)

        
        self.pulse_input=TextInput(multiline = False)
        self.pulse_input.set_disabled(True)
        Vlayout.add_widget(self.sec)
        Hlayout1.add_widget(self.pulse_input)

        Vlayout.add_widget(Hlayout1)

        Hlayout2 = BoxLayout(size_hint=(.8,None),height = '30sp')
        self.btn_ok=Button(text='Начать',size_hint=(.3,.2),pos_hint={'center_x':0.5})
        self.btn_ok.on_press= self.next
        Vlayout.add_widget(self.btn_ok)

        self.add_widget(Vlayout)
    
    def sec_finished(self,*args):
        self.pulse_input.set_disabled(False)
        self.btn_ok.set_disabled(False)
        self.btn_ok.text = 'Продолжить'
        self.next_screen = True
    def next(self):
        if self.next_screen == True:
            global p1
            p1 = self.pulse_input.text
            p1 = check_int(p1)
            if p1 == False or p1 <= 0 :
                p1 = 0
                self.pulse_input.text = str(p1)
            else:
                self.manager.current='third'
        else:
            self.btn_ok.set_disabled(True)
            self.sec.start()

class ThirdScr(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.next_screen = False
        self.runnerclass = Runner(total = 30, steptime = 1.5)
        self.runnerclass.bind(finished=self.run_finished)
        self.sitsclass = Sits(30)
        Hlayout = BoxLayout()

        Vlayout = BoxLayout(orientation = 'vertical')
        lbl=Label(text=txt_sits)
        Hlayout.add_widget(lbl)
        Hlayout.add_widget(self.sitsclass)
        Hlayout.add_widget(self.runnerclass)
        self.btn_ok=Button(text='Начать',size_hint=(.3,.2),pos_hint={'center_x':0.5})
        self.btn_ok.on_press=self.next
        Vlayout.add_widget(Hlayout)
        Vlayout.add_widget(self.btn_ok)
       
        self.add_widget(Vlayout)
    
    def run_finished(self, *args):
        self.next_screen = True
        self.btn_ok.set_disabled(False)
        self.btn_ok.text = 'Продолжить'

    def next(self):
        if self.next_screen == True:
            self.manager.current='fourth'
        else:
            self.btn_ok.set_disabled(True)
            self.runnerclass.start()
            print(1)
            self.runnerclass.bind(value=self.sitsclass.next)
            print(2)

class FourthScr(Screen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.next_screen = False
        self.stage = 0
        Vlayout = BoxLayout(orientation='vertical')
        insrt_lbl = Label(text=txt_test3)
        Hlayout1 = BoxLayout(size_hint=(.8,None),height = '30sp')
        first_lbl = Label(text='Результат:')
        second_lbl = Label(text='Результат после отдыха:')
        self.sec = Seconds(15)
        self.sec.bind(done = self.sec_finished)
        self.first_input = TextInput(multiline = False)
        self.first_input.set_disabled(True)
        self.second_input = TextInput(multiline = False)
        self.second_input.set_disabled(True)
        
        Vlayout.add_widget(insrt_lbl)
        Vlayout.add_widget(self.sec)
        Hlayout2 = BoxLayout(size_hint=(.8,None),height = '30sp')

        self.btn_ok = Button(text='Начать',size_hint=(.3,.2),pos_hint={'center_x':0.5})
        self.btn_ok.on_press = self.next
        
        Hlayout1.add_widget(first_lbl)
        Hlayout2.add_widget(second_lbl)
        Hlayout1.add_widget(self.first_input)
        Hlayout2.add_widget(self.second_input)
        Vlayout.add_widget(Hlayout1)
        Vlayout.add_widget(Hlayout2)
        Vlayout.add_widget(self.btn_ok)
        

        self.add_widget(Vlayout)

    def sec_finished(self,*args):
        if self.sec.done:
            if self.stage == 0:
                self.stage = 1
                self.sec.restart(30)
                self.first_input.set_disabled(False)
            elif self.stage == 1:
                self.stage = 2
                self.sec.restart(15)
            elif self.stage == 2:
                self.second_input.set_disabled(False)
                self.btn_ok.set_disabled(False)
                self.btn_ok.text = 'Продолжить'
                self.next_screen = True
    def next(self):
        if self.next_screen == True:
            global p2, p3
            p2 = self.first_input.text
            p3 = self.second_input.text
            p2 = check_int(p2)
            p3 = check_int(p3)
            if p2 == False or p2 <= 0:
                p2 = 0
                self.first_input.text = str(p2)
            elif p3 == False or p3 <= 0:
                p3 = 0
                self.second_input.text = str(p3)
            else:
                self.manager.current='fifth'
        else:
            self.btn_ok.set_disabled(True)
            self.sec.start()

class FifthScr(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Vlayout = BoxLayout(orientation='vertical')
        self.lbl = Label(text='лйбл')
        Vlayout.add_widget(self.lbl)
        self.on_enter = self.next
        self.add_widget(Vlayout)

    def next(self):
        self.lbl.text = name + ', ' + test(int(p1),int(p2),int(p3),int(age))
class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(FirstScr(name = 'first'))
        sm.add_widget(SecondScr(name = 'second'))
        sm.add_widget(ThirdScr(name = 'third'))
        sm.add_widget(FourthScr(name = 'fourth'))
        sm.add_widget(FifthScr(name = 'fifth'))
        return sm

app = MyApp()
app.run()