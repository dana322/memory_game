import sys
import os

rootdir = os.path.split(os.path.abspath(__file__))[0]
sys.path.append(os.path.join(rootdir, "utils"))
sys.path.append(os.path.join(rootdir, "src"))

from memorg_game import FlipCardByMemoryGame

game = FlipCardByMemoryGame()

game.run()