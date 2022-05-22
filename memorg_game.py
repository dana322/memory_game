from asyncio import constants
from cProfile import label
from pkgutil import extend_path
from shelve import Shelf
from statistics import mean
import tkinter
from venv import create
from xmlrpc.client import boolean
import pygame
import os
import random
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import sys
rootdir = os.path.split(os.path.abspath(__file__))[0]
sys.path.append(os.path.join(rootdir, "utils"))
sys.path.append(os.path.join(rootdir, "src"))
sys.path.append(os.path.join(rootdir, "constant"))
print("DEBUG:{}".format(os.path.join(rootdir, "constant")))


from config import Config
from playbgm import playbgm
from check import check
from menu import create_menu
from constant import advanced_constants
from constant import junior_constants
from constant import mediate_constants


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
        self.guest_login_button = Button(self.login_window, text="游客登录", command=self.run_junior)
        self.guest_login_button.pack()
    
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
        self.root.title('Flip Card by Memory')
        # 游戏界面中的卡片字典
        self.game_matrix = {}
        # 背景图像
        self.blank_image = PhotoImage(data=cfg.IMAGEPATHS['blank'])
        # 卡片背面
        self.cards_back_image = PhotoImage(data=cfg.IMAGEPATHS['cards_back'])
        # 所有卡片的索引
        cards_list = list(range(image_num - 1)) + list(range(image_num - 1))
        random.shuffle(cards_list)
        # 在界面上显示所有卡片的背面
        for r in range(line):
            for c in range(column):
                position = f'{r}_{c}'
                self.game_matrix[position] = Label(self.root, image=self.cards_back_image)
                self.game_matrix[position].back_image = self.cards_back_image
                self.game_matrix[position].file = str(cards_list[r * line + c])
                # print("SHOW: r is {}, r * 4 is {}, c is {}, r * 4 + c is {}".format(r, r * 4, c, r * 4 + c))
                print("DEBUG:{}".format(self.game_matrix[position].file))
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




    def run_junior(self):
        self.create_game_window()

    def run_mediate(self):
        self.create_game_window(mediate_constants.MEDIATE_IMAGE_NUM, mediate_constants.MEDIATE_LINE, mediate_constants.MEDIATE_COLUMN, mediate_constants.MEDIATE_RANK)

    def run_advanced(self):
        self.create_game_window(advanced_constants.MEDIATE_IMAGE_NUM, advanced_constants.MEDIATE_LINE, advanced_constants.MEDIATE_COLUMN, advanced_constants.MEDIATE_RANK)

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
            else: self.root.destroy()

        '''重新开始游戏'''
    def restart(self):
        self.root.destroy()
        client = FlipCardByMemoryGame()
        # TODO:重新开始的是啥的问题
        client.run()

    
a = FlipCardByMemoryGame()
a.run()