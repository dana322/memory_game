from tkinter import Menu

def create_menu(self):
    '''主菜单'''

    # 主菜单句柄
    self.main_menu = Menu(self.root)
    # 下拉菜单句柄
    self.rank_menu = Menu(self.main_menu, tearoff=False)
    self.choose_difficulty_menu = Menu(self.main_menu, tearoff=False)

    # 难度子菜单
    self.choose_difficulty_menu.add_command(label="初级", command=self.run_junior)
    self.choose_difficulty_menu.add_command(label="中级", command=self.run_mediate)
    self.choose_difficulty_menu.add_command(label="高级", command=self.run_advanced)
    self.main_menu.add_cascade(label="选择难度", menu=self.choose_difficulty_menu)

    # 排行榜子菜单
    self.rank_menu.add_command(label="初级排行榜", command=self.junior_window)
    self.rank_menu.add_command(label="中级排行榜", command=self.mediate_window)
    self.rank_menu.add_command(label="高级排行榜", command=self.advanced_window)
    self.main_menu.add_cascade(label='查看排行榜', menu=self.rank_menu)
    
    # 显示主菜单
    self.root.config(menu=self.main_menu)