'''播放背景音乐'''
import pygame


def playbgm(self):

    pygame.init()
    # mixer：用于加载和播放声音的pygame模块
    # initialize the mixer module
    pygame.mixer.init()
    # mixer.music: pygame module for controlling streamed audio
    # Load a music file for playback
    pygame.mixer.music.load(self.cfg.AUDIOPATHS['bgm'])
    # Start the playback of the music stream
    # play(loops=0, start=0.0, fade_ms=0) -> None
    # loops indicates how many times to repeat the music. 
    # The music repeats indefinitely if this argument is set to -1.
    pygame.mixer.music.play(-1, 0.0)