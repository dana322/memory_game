from asyncio import constants
from cProfile import label
from pkgutil import extend_path
from shelve import Shelf
from shutil import which
from statistics import mean
import tkinter
from venv import create
from xmlrpc.client import boolean
from colorama import Cursor
from kiwisolver import Expression
from numpy import insert
import pygame
import os
import random
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import pymysql
import sys
rootdir = os.path.split(os.path.abspath(__file__))[0]
sys.path.append(os.path.join(rootdir, "utils"))
sys.path.append(os.path.join(rootdir, "src"))
sys.path.append(os.path.join(rootdir, "constant"))
# print("DEBUG:{}".format(os.path.join(rootdir, "constant")))


from config import Config
from playbgm import playbgm
from menu import create_menu
from constant import advanced_constants
from constant import junior_constants
from constant import mediate_constants
from rank import ranking_window

'''记忆翻牌小游戏'''
class FlipCardByMemoryGame():
    def __init__(self):
        self.cfg = Config
        self.create_login_window()

        # 数据库
        self.db = pymysql.connect(host='localhost', port=3306, user='debian-sys-maint', passwd='123456', database='ranking')
        self.db_cursor = self.db.cursor()

        # 难度标识 0 初级 1 中级 2 高级
        self.which_game = 0

    def create_login_window(self):
        # 主界面句柄
        self.login_window = Tk()
        self.login_window.title('Flip Card by Memory')   
        # TODO: 图标
        # self.login_window.iconbitmap('/home/danan/item/demo/resources/cat.ico') 
        self.login_window.geometry('450x300')
        # 新建文本标签
        # TODO: 用户名
        self.username = Label(self.login_window)
        # 创建动字符串
        self.entry = Entry(self.login_window)
        Dy_String = StringVar()
        self.entry["textvariable"] = Dy_String
        self.login_button = Button(self.login_window, text="登录", command=self.login_click_callback)
        self.entry.focus()
        self.entry.pack()
        self.username.pack(side='left')
        self.login_button.pack(side='right')
        self.login_window.update()

        # print("SHOW:{}".format(Dy_String.get()))
        # Dy_String = StringVar()
        # self.entry2 = Entry(self.login_window,textvariable =Dy_String,validate ="none",validatecommand= self.check)
        # self.entry2.pack()
        # 登录按钮
        self.login_button.pack()

        # 创建游客登录按钮
        # TODO:grid布局
        # TODO: runjunior
        self.guest_login_button = Button(self.login_window, text="游客登录", command=self.run_junior)
        self.guest_login_button.pack()

        
        # 居中显示
        # TODO: login居中显示
        self.login_window.withdraw()
        self.login_window.update_idletasks()
        x = (self.login_window.winfo_screenwidth() - self.login_window.winfo_reqwidth()) / 2
        y = (self.login_window.winfo_screenheight() - self.login_window.winfo_reqheight()) / 2
        self.login_window.geometry('+%d+%d' % (x, y))
        self.login_window.deiconify()
    
    '''help function'''
    def help(self):
        print('000000')

    '''游戏界面'''
    # TODO:游戏菜单
    def create_game_window(self, image_num = junior_constants.JUNIOR_IMAGE_NUM, line = junior_constants.JUNIOR_LINE, column = junior_constants.JUNIOR_COLUMN, rank = junior_constants.JUNIOR_RANK):
        try:
            self.login_window.destroy()
        except BaseException as err:
            print(f"Unexpected {err=}, {type(err)=}")

        try:
            self.root.destroy()
        except BaseException as err:
            print(f"Unexpected {err=}, {type(err)=}")

        # 计时器flag
        self.is_first_click = 0

        self.root = Tk()
        # 创建菜单
        create_menu(self)
        cfg = self.cfg
        # 播放背景音乐
        playbgm(self)
        # 载入得分后响起的音乐
        # Create a new Sound object from a file or buffer object
        # Sound(filename) -> Sound
        self.score_sound = pygame.mixer.Sound(cfg.AUDIOPATHS['score'])
        # set the playback volume for this Sound
        self.score_sound.set_volume(1)
        # 卡片图片路径
        self.card_dir = cfg.IMAGEPATHS['carddirs'][rank]
        print(self.card_dir)
        self.root.title('Flip Card by Memory')
        # 游戏界面中的卡片字典
        self.game_matrix = {}
        # 背景图像
        self.blank_image = PhotoImage(data=cfg.IMAGEPATHS['blank'])
        # 卡片背面
        self.cards_back_image = PhotoImage(data=cfg.IMAGEPATHS['cards_back'])
        # 所有卡片的索引
        cards_list = list(range(image_num)) + list(range(image_num))
        print("cardlist{}".format(cards_list))
        random.shuffle(cards_list)
        # 在界面上显示所有卡片的背面
        for r in range(line):
            for c in range(column):
                position = f'{r}_{c}'
                self.game_matrix[position] = Label(self.root, image=self.cards_back_image)
                self.game_matrix[position].back_image = self.cards_back_image
                # r*colmn+c生成0-cards_num个数
                self.game_matrix[position].file = str(cards_list[r * column + c])
                # print("SHOW:{}".format(self.game_matrix[position].file))
                # print("SHOW: r is {}, r * column is {}, c is {}, r * colume + c is {}".format(r, r * column, c, r * column + c))
                # print("DEBUG:{}".format(self.game_matrix[position].file))
                self.game_matrix[position].show = False
                self.game_matrix[position].bind('<Button-1>', self.clickcallback)
                self.game_matrix[position].grid(row=r, column=c)
        # 已经显示正面的卡片
        self.shown_cards = []
        # 场上存在的卡片数量
        self.num_existing_cards = len(cards_list)
        # 显示游戏时间
        self.num_seconds = 0
        self.time = Label(self.root, text=f'Time Left: {self.num_seconds}')
        self.time.grid(row=line + 1, column=column - 1, columnspan=2)
        # 显示用户
        self.user_name = ''
        try:
            self.user_name = self.input_name
        except:
            self.user_name = '游客'
        self.greet = Label(self.root, text=f'欢迎你! {self.user_name}')
        self.greet.grid(row=line + 1, column=0)
        # 居中显示
        self.root.withdraw()
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - self.root.winfo_reqwidth()) / 2
        y = (self.root.winfo_screenheight() - self.root.winfo_reqheight()) / 2
        self.root.geometry('+%d+%d' % (x, y))
        self.root.deiconify()
        # 显示主界面
        self.run_game()



    # 把几个run规范一下
    def run_junior(self):
        self.which_game = 0
        self.create_game_window()

    def run_mediate(self):
        self.which_game = 1
        self.create_game_window(mediate_constants.MEDIATE_IMAGE_NUM, mediate_constants.MEDIATE_LINE, mediate_constants.MEDIATE_COLUMN, mediate_constants.MEDIATE_RANK)

    def run_advanced(self):
        self.which_game = 2
        self.create_game_window(advanced_constants.ADVANCED_IMAGE_NUM, advanced_constants.ADVANCED_LINE, advanced_constants.ADVANCED_COLUMN, advanced_constants.ADVANCED_RANK)

    '''运行游戏'''
    def run_game(self):
        self.root.mainloop()
    
    def rander_window(self, rank):
        try:
            print(f"select * from '{rank}'")
            self.db_cursor.execute(f"select * from {rank} order by score desc limit 10")
            data = self.db_cursor.fetchall()
            ranking_window(self, data)
        except:
            print('error')

    def junior_window(self):
        self.rander_window('junior_ranking')
    
    def mediate_window(self):
        self.rander_window('mediate_ranking')
    
    def advanced_window(self):
        self.rander_window('advanced_ranking')


    '''运行程序'''
    def run(self):
        # 显示主界面
        self.login_window.mainloop()

    '''点击回调函数'''
    def clickcallback(self, event):
        # 第一次点击任意卡片，计时器开始
        if self.is_first_click == 0:
            self.is_first_click = 1
            self.tick()
        card = event.widget
        # print(card)
        if card.show: 
            return
        # 之前没有卡片被翻开
        if len(self.shown_cards) == 0:
            self.shown_cards.append(card)
            image = ImageTk.PhotoImage(Image.open(os.path.join(self.card_dir, card.file+'.png')))
            card.configure(image=image)
            card.show_image = image
            card.show = True
        # 之前只有一张卡片被翻开
        elif len(self.shown_cards) == 1:
            # --之前翻开的卡片和现在的卡片一样
            if self.shown_cards[0].file == card.file:
                def delaycallback():
                    self.shown_cards[0].configure(image=self.blank_image)
                    self.shown_cards[0].blank_image = self.blank_image
                    card.configure(image=self.blank_image)
                    card.blank_image = self.blank_image
                    self.shown_cards.pop(0)
                    self.score_sound.play()
                image = ImageTk.PhotoImage(Image.open(os.path.join(self.card_dir, card.file+'.png')))
                card.configure(image=image)
                card.show_image = image
                card.show = True
                card.after(300, delaycallback)
                self.num_existing_cards -= 2
            # --之前翻开的卡片和现在的卡片不一样
            else:
                self.shown_cards.append(card)
                image = ImageTk.PhotoImage(Image.open(os.path.join(self.card_dir, card.file+'.png')))
                card.configure(image=image)
                card.show_image = image
                card.show = True
        # 之前有两张卡片被翻开
        elif len(self.shown_cards) == 2:
            # --之前翻开的第一张卡片和现在的卡片一样
            if self.shown_cards[0].file == card.file:
                def delaycallback():
                    self.shown_cards[0].configure(image=self.blank_image)
                    self.shown_cards[0].blank_image = self.blank_image
                    card.configure(image=self.blank_image)
                    card.blank_image = self.blank_image
                    self.shown_cards.pop(0)
                    self.score_sound.play()
                self.num_existing_cards -= 2
                image = ImageTk.PhotoImage(Image.open(os.path.join(self.card_dir, card.file+'.png')))
                card.configure(image=image)
                card.show_image = image
                card.show = True
                card.after(300, delaycallback)
            # --之前翻开的第二张卡片和现在的卡片一样
            elif self.shown_cards[1].file == card.file:
                def delaycallback():
                    self.shown_cards[1].configure(image=self.blank_image)
                    self.shown_cards[1].blank_image = self.blank_image
                    card.configure(image=self.blank_image)
                    card.blank_image = self.blank_image
                    self.shown_cards.pop(1)
                    self.score_sound.play()
                self.num_existing_cards -= 2
                image = ImageTk.PhotoImage(Image.open(os.path.join(self.card_dir, card.file+'.png')))
                card.configure(image=image)
                card.show_image = image
                card.show = True
                card.after(300, delaycallback)
            # --之前翻开的卡片和现在的卡片都不一样
            else:
                self.shown_cards.append(card)
                self.shown_cards[0].configure(image=self.cards_back_image)
                self.shown_cards[0].show = False
                self.shown_cards.pop(0)
                image = ImageTk.PhotoImage(Image.open(os.path.join(self.card_dir, card.file+'.png')))
                self.shown_cards[-1].configure(image=image)
                self.shown_cards[-1].show_image = image
                self.shown_cards[-1].show = True
        # 判断游戏是否已经胜利
        # print("existing cards:{}".format(self.num_existing_cards))
        if self.num_existing_cards == 0:
            self.insert_grade()
            is_restart = messagebox.askyesno('Game Over', 'Congratulations, you win, do you want to play again?')
            if is_restart: self.restart()
            else: self.root.destroy()
    
    '''插入成绩'''
    def insert_grade(self):
        time = str(self.num_seconds)
        try:
            if self.which_game == 0:
                self.db_cursor.execute(f"insert into junior_ranking values(null, '{time}', '{self.user_name}');")
            elif self.which_game == 1:
                self.db_cursor.execute(f"insert into mediate_ranking values(null, '{time}', '{self.user_name}');")
            elif self.which_game == 2:
                self.db_cursor.execute(f"insert into advanced_ranking values(null, '{time}', '{self.user_name}');")
            self.db.commit()
        except:
            self.db.rollback()
    
    '''计时'''
    def tick(self):
        # print(111)
        if self.num_existing_cards == 0: return
        # print(222)
        self.num_seconds += 1
        self.time['text'] = f'Time Left: {self.num_seconds}'
        self.time.after(1000, self.tick)
        

        '''重新开始游戏'''
    
    def restart(self):
        self.root.destroy()
        client = FlipCardByMemoryGame().run_junior()

    '''检查'''
    def login_click_callback(self):
        if 0 < len(self.entry.get()) <= 8:
            self.input_name = self.entry.get()
            self.run_junior()
            return True
        else:
            messagebox.showwarning("输入不正确")
            self.entry.delete(0, tkinter.END)
            return False

    
a = FlipCardByMemoryGame()
a.run()