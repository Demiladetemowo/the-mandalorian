import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
import random
from time import monotonic as clock

import config as conf
from thing import Thing

class Mandalorian(Thing):

    def __init__(self, game_height, game_width, y=0):

        super().__init__(game_height, game_width, np.array([game_height - conf.GND_HEIGHT - 4, y]), np.array([4, 3]))
        self.acc = np.array([conf.GRAVITY_X, conf.GRAVITY_Y])
        self.repr = np.array([
            [' ', '_', ' '],
            ['|', 'O', '`'],
            ['[', ' ', ']'],
            [' ', 'J', 'L']
        ], dtype='object')

    def nudge(self, key):
        if key == 'w':
            self.acc[0] -= conf.KEY_FORCE
        elif key == 'a':
            self.acc[1] -= conf.KEY_FORCE
        elif key == 'd':
            self.acc[1] += conf.KEY_FORCE

    def calc_acc(self):
        super().calc_acc()

        self.acc[0] += conf.GRAVITY_X
        self.acc[1] += conf.GRAVITY_Y

        if (self.vel[1] + conf.GAME_SPEED) > 0:
            drag = -conf.DRAG_COEFF * ((self.vel[1] + conf.GAME_SPEED)** 2)
        else:
            drag = conf.DRAG_COEFF * ((self.vel[1] + conf.GAME_SPEED)** 2)
            
        self.acc[1] += drag