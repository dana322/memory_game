'''播放背景音乐'''
import pygame

def playbgm(self):
    '''播放音乐'''
    
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(self.cfg.AUDIOPATHS['bgm'])
    pygame.mixer.music.play(-1, 0.0)