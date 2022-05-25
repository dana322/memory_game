import tkinter
import pygame
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import pymysql

import sys
import os
import random

rootdir = os.path.split(os.path.abspath(__file__))[0]
sys.path.append(os.path.join(rootdir, "utils"))
sys.path.append(os.path.join(rootdir, "src"))
sys.path.append(os.path.join(rootdir, "constant"))

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
        '''构造方法'''
        self.cfg = Config
        # 创建登录窗口
        self.create_login_window()

        # 数据库
        self.db = pymysql.connect(host='localhost', port=3306, user='debian-sys-maint', passwd='123456', database='ranking')
        self.db_cursor = self.db.cursor()

        # 难度标识 0 初级 1 中级 2 高级
        self.which_game = 0

    def create_login_window(self):
        '''创建登录窗口'''
        # 主界面句柄
        self.login_window = Tk()
        # 窗口名字
        self.login_window.title('Flip Card by Memory')  
        # 不可拖动窗口 
        self.login_window.resizable(0, 0)
        # 窗口大小
        self.login_window.geometry('450x300')
        username = Label(self.login_window, text='用户名:', width=10)
        # 创建动字符串 和entry控件
        self.entry = Entry(self.login_window)
        Dy_String = StringVar()
        self.entry["textvariable"] = Dy_String
        # 登录按钮
        login_button = Button(self.login_window, text="登录", command=self.login_click_callback)

        # 创建游客登录按钮
        self.guest_login_button = Button(self.login_window, text="游客登录", command=self.run_junior)

        # 布局 
        username.place(x=80, y=100)
        self.entry.place(x=150, y=100)
        login_button.place(x=130, y=150)
        self.guest_login_button.place(x=190, y=150)

        # login窗口刷新，获取用户输入
        self.login_window.update()
        
        # 窗口显示位置
        self.login_window.withdraw()
        self.login_window.update_idletasks()
        x = (self.login_window.winfo_screenwidth() - self.login_window.winfo_reqwidth()) / 2
        y = (self.login_window.winfo_screenheight() - self.login_window.winfo_reqheight()) / 2
        self.login_window.geometry('+%d+%d' % (x, y))
        self.login_window.deiconify()
    

    def create_game_window(self, image_num = junior_constants.JUNIOR_IMAGE_NUM, line = junior_constants.JUNIOR_LINE, column = junior_constants.JUNIOR_COLUMN, rank = junior_constants.JUNIOR_RANK):
        '''游戏界面'''

        # 如果有窗口在运行，销毁
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
        
        # 窗口句柄
        self.root = Tk()
        # 不可拖动窗口
        self.root.resizable(0, 0)
        # 创建菜单
        create_menu(self)
        cfg = self.cfg

        # 播放背景音乐
        playbgm(self)
        # 载入得分后响起的音乐
        self.score_sound = pygame.mixer.Sound(cfg.AUDIOPATHS['score'])
        self.score_sound.set_volume(1)

        # 卡片图片路径
        self.card_dir = cfg.IMAGEPATHS['carddirs'][rank]
        self.root.title('Flip Card by Memory')
        # 游戏界面中的卡片字典
        self.game_matrix = {}
        # 背景图像
        self.blank_image = PhotoImage(data=cfg.IMAGEPATHS['blank'])
        # 卡片背面
        self.cards_back_image = PhotoImage(data=cfg.IMAGEPATHS['cards_back'])
        # 所有卡片的索引
        cards_list = list(range(image_num)) + list(range(image_num))
        random.shuffle(cards_list)

        # 在界面上显示所有卡片的背面
        for r in range(line):
            for c in range(column):
                position = f'{r}_{c}'
                self.game_matrix[position] = Label(self.root, image=self.cards_back_image)
                self.game_matrix[position].back_image = self.cards_back_image
                # r*colmn+c生成0-cards_num个数
                self.game_matrix[position].file = str(cards_list[r * column + c])
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

    def run_junior(self):
        '''运行初级游戏'''
        self.which_game = 0
        self.create_game_window()

    def run_mediate(self):
        '''运行中级游戏'''
        self.which_game = 1
        self.create_game_window(mediate_constants.MEDIATE_IMAGE_NUM, mediate_constants.MEDIATE_LINE, mediate_constants.MEDIATE_COLUMN, mediate_constants.MEDIATE_RANK)

    def run_advanced(self):
        '''运行高级游戏'''
        self.which_game = 2
        self.create_game_window(advanced_constants.ADVANCED_IMAGE_NUM, advanced_constants.ADVANCED_LINE, advanced_constants.ADVANCED_COLUMN, advanced_constants.ADVANCED_RANK)

    def run_game(self):
        '''显示游戏主界面'''
        self.root.mainloop()

    def run(self):
        '''显示登录页面的主界面'''
        self.login_window.mainloop()

    def rander_window(self, rank):
        '''渲染排行榜界面，查询数据库数据放入界面中'''
        try:
            # TODO: 排序
            self.db_cursor.execute(f"select * from {rank} order by score desc limit 10")
            data = self.db_cursor.fetchall()
            ranking_window(self, data)
        except:
            print('error')

    def junior_window(self):
        '''渲染初级排行榜'''
        self.rander_window('junior_ranking')
    
    def mediate_window(self):
        '''渲染中级排行榜'''
        self.rander_window('mediate_ranking')
    
    def advanced_window(self):
        '''渲染高级排行榜'''
        self.rander_window('advanced_ranking')

    '''点击回调函数'''
    def clickcallback(self, event):
        # 第一次点击任意卡片，计时器开始
        if self.is_first_click == 0:
            self.is_first_click = 1
            self.tick()
        card = event.widget
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
        if self.num_existing_cards == 0: return
        self.num_seconds += 1
        self.time['text'] = f'Time Left: {self.num_seconds}'
        self.time.after(1000, self.tick)
        
    def restart(self):
        '''重新运行游戏'''
        self.root.destroy()
        FlipCardByMemoryGame().run_junior()

    def login_click_callback(self):
        '''登录按钮的回调函数
            1.检查用户输入名字是否合法, 0 < 用户名长度 <= 8 
            2.如果合法,进入游戏
        '''
        if 0 < len(self.entry.get()) <= 8:
            self.input_name = self.entry.get()
            self.run_junior()
            return True
        else:
            messagebox.showwarning("输入不正确")
            self.entry.delete(0, tkinter.END)
            return False



