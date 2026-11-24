from game_logic_2_0 import Game_logic
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Color, Line
from kivy.core.window import Window
Window.size = (450,800)


class Main_app(App):

    def build(self):
        self.hod = 'X/O'
        self.XO = True
        self.IQ_ai = 0.5
        self.anch = AnchorLayout(anchor_x = 'center',anchor_y = 'center')
        self.Bot_ferst = True
        self.bot_count,self.you_count = 0,0
        self.bot_cunter , self.you_counter= Label(size_hint = (0.3,0.2),text = f'Бот: {self.bot_count}',pos_hint={"center_x": 0.75, "y": 0.8},font_size=30),Label(size_hint = (0.3,0.2),text = f'Ты: {self.you_count}',pos_hint={"center_x": 0.25, "y": 0.8},font_size=30)
        self.root = FloatLayout()
        self.gameplay = True
        self.game = Game_logic('ww_beast.pkl')
        self.button_pole = {}
        self.creat_pole()
        reset = Button(size_hint = (0.3,0.1),text = '[color=ff3333]Reset[/color]',on_press = self.reset,pos_hint={"center_x": 0.25, "y": 0.1},font_size = 30,markup = True)
        ch_hd = Button(size_hint = (0.3,0.1),text = 'X/O',on_press = self.switch_Bot,pos_hint={"center_x": 0.25, "y": 0.75},font_size=30)
        self.root.add_widget(Button(size_hint = (0.3,0.1),text = 'легко',color = 'green',on_press = self.swich_bot_skill,pos_hint={"center_x": 0.75, "y": 0.75},font_size=30))
        self.root.add_widget(self.you_counter)
        self.root.add_widget(self.bot_cunter)
        self.root.add_widget(reset)
        self.root.add_widget(ch_hd)
        self.line = Line(points=[0, 0, 100, 0], width=1.5)
        self.anch   
        self.Bot()
        self.root.add_widget(self.anch)
        return self.root

    def swich_bot_skill(self,inc):
        if inc.text == 'легко':
            inc.text = 'норм'
            inc.color = "orange"
            self.IQ_ai = 0.2
        elif inc.text == 'норм':
            inc.text = 'сложно'
            inc.color = "red"
            self.IQ_ai = 0.01
        elif inc.text == 'сложно':
            inc.text = 'легко'
            inc.color = 'green'
            self.IQ_ai = 0.5


    def switch_Bot(self,btn):

        if btn.text == 'X/O':
            btn.text = 'Бот'
            self.hod = 'Бот'
        elif btn.text == 'Бот':
            btn.text = 'Ты'
            self.hod = 'Ты'
        elif btn.text == 'Ты':
            btn.text == 'X/O'
            self.hod = 'X/O'
        self.reset(btn)

    def Bot(self):
        if self.hod == 'Бот':
            self.ai_press()
        elif self.hod == 'X/O':
            if self.XO:
                self.ai_press()
            self.XO = not self.XO


    def creat_pole(self):
        
        a = GridLayout(rows = 3,cols = 3,size_hint = (0.8,0.45))
        for i in range(1,10):
            row,col = ((i-1)//3)+1, ((i-1)%3)+1
            btn = Button(on_press = self.press_player,font_size=50)
            btn.row,btn.col = row,col
            self.button_pole[(row,col)] = btn
            a.add_widget(btn)
        self.anch.add_widget(a)

    def reset(self,inc):
        self.gameplay = True
        self.game.reset()
        self.line.points=[-1, -1, -1, -1]
        for btn in self.button_pole.values():
            btn.text = ""
        
        self.Bot()

    def detct_end_game(self):

        b1,b2,b3= self.game.detect_win()

        if b1!= 0:
            self.line_draw(b1,b2,b3)
            self.gameplay = False
            if self.button_pole[b1[0],b1[1]].text == 'X':
                self.bot_count += 1
                self.bot_cunter.text = f'Бот: {str(self.bot_count)} '
            elif self.button_pole[b1[0],b1[1]].text == 'O' :
                self.you_count +=1
                self.you_counter.text = f'Ты: {str(self.you_count)}'
        elif not self.game.is_game():
            self.gameplay = False


    def line_draw(self,b1,b2,b3):

        x1,y1 =self.button_pole[b1].to_window(self.button_pole[b1].center_x,self.button_pole[b1].center_y)
        x2,y2 =self.button_pole[b2].to_window(self.button_pole[b2].center_x,self.button_pole[b2].center_y)
        x3,y3 =self.button_pole[b3].to_window(self.button_pole[b3].center_x,self.button_pole[b3].center_y)

        with self.root.canvas:
            Color(1, 0, 0, 1)
            self.line = Line(points=[x2, y2, x3, y3], width=3)
            


    def press_player(self,instance):
        if not self.gameplay:
            return
        if not self.game.move(row=instance.row,col=instance.col,pl=-1) :
            return
        instance.text = 'O'
        instance.color = "green"
        self.detct_end_game()
        self.ai_press()

    def ai_press(self):
        if not self.gameplay:
                    ('end game')
                    return
        a = self.game.ai_hod(pl=1,eps=self.IQ_ai)
        (not self.gameplay)
        self.game.move(row=a[0],col=a[1],pl=1)
        self.button_pole[(a[0],a[1])].text = 'X'
        self.button_pole[(a[0],a[1])].color = "red"
        self.detct_end_game()

Main_app().run()
