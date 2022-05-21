from cProfile import label
import imp
from shelve import Shelf
import tkinter
from venv import create
import pygame
import os
import random
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import sys
sys.path.append("/home/danan/item/flash-demo/utils")

from config import Config
from playbgm import playbgm
from check import check



'''记忆翻牌小游戏'''
class FlipCardByMemoryGame():
    def __init__(self):
        self.cfg = Config
        self.create_login_window()

    def create_login_window(self):
        # 主界面句柄
        self.login_window = Tk()
        self.login_window.title('Flip Card by Memory')    
        self.login_window.geometry('450x300')
        # 新建文本标签
        self.username = Label(self.login_window, text = "用户名：")
        self.username.pack()
        # 创建动字符串
        Dy_String = StringVar()
        self.entry = Entry(self.login_window,textvariable =Dy_String,validate ="focusout",validatecommand= check)
        self.entry.pack()
        # 创建游客登录按钮
        # TODO:grid布局
        self.guest_login_button = Button(self.login_window, text="游客登录", command=self.create_game_window)
        self.guest_login_button.pack()

    '''游戏界面'''
    # TODO:游戏菜单
    def create_game_window(self):
        print('111')


        self.login_window.destroy()
        # self.root = Toplevel(self.login_window)
        self.root = Tk()
        self.main_menu = Menu(self.root)
        # TODO:排行榜页面
        self.main_menu.add_command (label="选择难度",command=self.menuCommand)
        self.main_menu.add_command (label="查看排行榜",command=self.menuCommand)
        self.root.config(menu=self.main_menu)
        cfg = self.cfg
        # 卡片图片路径
        self.card_dir = random.choice(cfg.IMAGEPATHS['carddirs'])
        # 播放背景音乐
        playbgm(self)
        # 载入得分后响起的音乐
        # Create a new Sound object from a file or buffer object
        # Sound(filename) -> Sound
        self.score_sound = pygame.mixer.Sound(cfg.AUDIOPATHS['score'])
        # set the playback volume for this Sound
        self.score_sound.set_volume(1)
        # 卡片图片路径
        self.card_dir = random.choice(cfg.IMAGEPATHS['carddirs'])
        # # 主界面句柄
        # self.root = Tk()
        # self.root.title('Flip Card by Memory')
        # 游戏界面中的卡片字典
        self.game_matrix = {}
        # 背景图像
        self.blank_image = PhotoImage(data=cfg.IMAGEPATHS['blank'])
        # 卡片背面
        self.cards_back_image = PhotoImage(data=cfg.IMAGEPATHS['cards_back'])
        # 所有卡片的索引
        cards_list = list(range(8)) + list(range(8))
        random.shuffle(cards_list)
        # 在界面上显示所有卡片的背面
        for r in range(4):
            for c in range(4):
                position = f'{r}_{c}'
                self.game_matrix[position] = Label(self.root, image=self.cards_back_image)
                self.game_matrix[position].back_image = self.cards_back_image
                self.game_matrix[position].file = str(cards_list[r * 4 + c])
                self.game_matrix[position].show = False
                self.game_matrix[position].bind('<Button-1>', self.clickcallback)
                self.game_matrix[position].grid(row=r, column=c)
        # 已经显示正面的卡片
        self.shown_cards = []
        # 场上存在的卡片数量
        self.num_existing_cards = len(cards_list)
        # 显示游戏剩余时间
        self.num_seconds = 30
        self.time = Label(self.root, text=f'Time Left: {self.num_seconds}')
        self.time.grid(row=6, column=3, columnspan=2)
        # 居中显示
        self.root.withdraw()
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - self.root.winfo_reqwidth()) / 2
        y = (self.root.winfo_screenheight() - self.root.winfo_reqheight()) / 2
        self.root.geometry('+%d+%d' % (x, y))
        self.root.deiconify()
        # 计时
        self.tick()
        self.run_game()





    '''运行游戏'''
    def run_game(self):
        self.root.mainloop()

    '''运行程序'''
    def run(self):
        # 显示主界面
        self.login_window.mainloop()

    '''点击回调函数'''
    def clickcallback(self, event):
        card = event.widget
        if card.show: return
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
                self.num_existing_cards -= 2
                image = ImageTk.PhotoImage(Image.open(os.path.join(self.card_dir, card.file+'.png')))
                card.configure(image=image)
                card.show_image = image
                card.show = True
                card.after(300, delaycallback)
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
            is_restart = messagebox.askyesno('Game Over', 'Congratulations, you win, do you want to play again?')
            if is_restart: self.restart()
            else: self.login_window.destroy()
    '''计时'''


    def tick(self):
        if self.num_existing_cards == 0: return
        if self.num_seconds != 0:
            self.num_seconds -= 1
            self.time['text'] = f'Time Left: {self.num_seconds}'
            self.time.after(1000, self.tick)
        else:
            is_restart = messagebox.askyesno('Game Over', 'You fail since time up, do you want to play again?')
            if is_restart: self.restart()
            else: self.login_window.destroy()

        '''重新开始游戏'''
    def restart(self):
        self.login_window.destroy()
        client = FlipCardByMemoryGame()
        client.run()

    
a = FlipCardByMemoryGame()
a.run()