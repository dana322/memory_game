# 播放背景音乐
        self.playbgm()
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