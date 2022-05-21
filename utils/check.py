'''检测用户名的函数'''
from tkinter import messagebox
import tkinter


def check(self):
    # TODO:用户重复验证
    if self.entry.get() == 'danan':
        # self.createGameWindow()
        print(self.entry.get())
        return True
    else:
        messagebox.showwarning("输入不正确")
        self.entry.delete(0, tkinter.END)
        return False