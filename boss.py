import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
import random
from time import monotonic as clock
import math

import config as conf
from thing import Thing
from obstacle import BossBullet

class Boss(Thing):
    def __init__(self, game_height, game_width):
        
        h = 15
        w = 39
        x = game_height - conf.GND_HEIGHT - h
        y = game_width - w - 4

        super().__init__(game_height, game_width, np.array([x, y], dtype='float32'), np.array([h, w]))

        self.vel = np.array([0, 0], dtype='float32')

        self.strength = conf.BOSS_MAX_STRENGTH

        self.repr = np.array([[' ', Style.BRIGHT + Fore.RED + '<', Style.BRIGHT + Fore.RED + '>', Style.BRIGHT + Fore.RED + '=', Style.BRIGHT + Fore.RED + '=', Style.BRIGHT + Fore.RED + '=', Style.BRIGHT + Fore.RED + '=', Style.BRIGHT + Fore.RED + '=', Style.BRIGHT + Fore.RED + '=', Style.BRIGHT + Fore.RED + '=', Style.BRIGHT + Fore.RED + '(',
        Style.BRIGHT + Fore.RED + ')', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
        ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
        ' ', ' ', ' ', ' ', ' ', ' '],
       [Style.BRIGHT + Fore.RED + '(', Style.BRIGHT + Fore.RED + '/', Style.BRIGHT + Fore.RED + '\\', Style.BRIGHT + Fore.RED + '_', Style.BRIGHT + Fore.RED + '_', Style.BRIGHT + Fore.RED + '_', ' ', ' ', ' ', Style.BRIGHT + Fore.RED + '/',
        Style.BRIGHT + Fore.RED + '|', Style.BRIGHT + Fore.RED + '\\', Style.BRIGHT + Fore.RED + '\\', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
        ' ', ' ', ' ', Style.BRIGHT + Fore.RED + '(', Style.BRIGHT + Fore.RED + ')', Style.BRIGHT + Fore.RED + '=', Style.BRIGHT + Fore.RED + '=', Style.BRIGHT + Fore.RED + '=', Style.BRIGHT + Fore.RED + '=', Style.BRIGHT + Fore.RED + '=', Style.BRIGHT + Fore.RED + '=',
        Style.BRIGHT + Fore.RED + '=', Style.BRIGHT + Fore.RED + '=', Style.BRIGHT + Fore.RED + '=', Style.BRIGHT + Fore.RED + '=', Style.BRIGHT + Fore.RED + '<', Style.BRIGHT + Fore.RED + '>', Style.BRIGHT + Fore.RED + '_', ' '],
       [' ', ' ', ' ', ' ', ' ', ' ', Style.BRIGHT + Fore.RED + '\\', Style.BRIGHT + Fore.RED + '_', Style.BRIGHT + Fore.RED + '/', ' ',
        Style.BRIGHT + Fore.RED + '|', ' ', Style.BRIGHT + Fore.RED + '\\', Style.BRIGHT + Fore.RED + '\\', ' ', ' ', ' ', ' ', ' ', ' ',
        ' ', ' ', Style.BRIGHT + Fore.RED + '/', Style.BRIGHT + Fore.RED + '/', Style.BRIGHT + Fore.RED + '|', Style.BRIGHT + Fore.RED + '\\', ' ', ' ', ' ', Style.BRIGHT + Fore.RED + '_',
        Style.BRIGHT + Fore.RED + '_', Style.BRIGHT + Fore.RED + '_', Style.BRIGHT + Fore.RED + '_', Style.BRIGHT + Fore.RED + '_', Style.BRIGHT + Fore.RED + '_', Style.BRIGHT + Fore.RED + '/', ' ', Style.BRIGHT + Fore.RED + '\\', Style.BRIGHT + Fore.RED + ')'],
       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', Style.BRIGHT + Fore.RED + '\\', Style.BRIGHT + Fore.RED + '_',
        Style.BRIGHT + Fore.RED + '|', ' ', ' ', Style.BRIGHT + Fore.RED + '\\', Style.BRIGHT + Fore.RED + '\\', ' ', ' ', ' ', ' ', ' ',
        ' ', Style.BRIGHT + Fore.RED + '/', Style.BRIGHT + Fore.RED + '/', ' ', Style.BRIGHT + Fore.RED + '|', ' ', Style.BRIGHT + Fore.RED + '\\', Style.BRIGHT + Fore.RED + '_', Style.BRIGHT + Fore.RED + '/', ' ',
        ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
        Style.BRIGHT + Fore.RED + '\\', Style.BRIGHT + Fore.RED + '|', Style.BRIGHT + Fore.RED + '\\', Style.BRIGHT + Fore.RED + '/', Style.BRIGHT + Fore.RED + '|', Style.BRIGHT + Fore.RED + '\\', Style.BRIGHT + Fore.RED + '_', ' ', ' ', ' ',
        Style.BRIGHT + Fore.RED + '/', Style.BRIGHT + Fore.RED + '/', ' ', ' ', Style.BRIGHT + Fore.RED + '/', Style.BRIGHT + Fore.RED + '\\', Style.BRIGHT + Fore.RED + '/', ' ', ' ', ' ',
        ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
        Style.BRIGHT + Fore.RED + '(', Style.BRIGHT + Fore.RED + 'o', Style.BRIGHT + Fore.RED + 'o', Style.BRIGHT + Fore.RED + ')', Style.BRIGHT + Fore.RED + '\\', ' ', Style.BRIGHT + Fore.RED + '\\', Style.BRIGHT + Fore.RED + '_', Style.BRIGHT + Fore.RED + '/', Style.BRIGHT + Fore.RED + '/',
        ' ', ' ', Style.BRIGHT + Fore.RED + '/', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
        ' ', ' ', ' ', ' ', ' ', ' ', ' '],
       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', Style.BRIGHT + Fore.RED + '/',
        Style.BRIGHT + Fore.RED + '/', Style.BRIGHT + Fore.RED + '_', Style.BRIGHT + Fore.RED + '/', Style.BRIGHT + Fore.RED + '\\', Style.BRIGHT + Fore.RED + '_', Style.BRIGHT + Fore.RED + '\\', Style.BRIGHT + Fore.RED + '/', ' ', Style.BRIGHT + Fore.RED + '/', ' ',
        ' ', Style.BRIGHT + Fore.RED + '|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
        ' ', ' ', ' ', ' ', ' ', ' ', ' '],
       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', Style.BRIGHT + Fore.RED + '@', Style.BRIGHT + Fore.RED + '@',
        Style.BRIGHT + Fore.RED + '/', ' ', ' ', Style.BRIGHT + Fore.RED + '|', Style.BRIGHT + Fore.RED + '=', Style.BRIGHT + Fore.RED + '\\', ' ', ' ', Style.BRIGHT + Fore.RED + '\\', ' ',
        ' ', Style.BRIGHT + Fore.RED + '|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
        ' ', ' ', ' ', ' ', ' ', ' ', ' '],
       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
        ' ', ' ', ' ', Style.BRIGHT + Fore.RED + '\\', Style.BRIGHT + Fore.RED + '_', Style.BRIGHT + Fore.RED + '=', Style.BRIGHT + Fore.RED + '\\', Style.BRIGHT + Fore.RED + '_', ' ', Style.BRIGHT + Fore.RED + '\\',
        ' ', Style.BRIGHT + Fore.RED + '|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
        ' ', ' ', ' ', ' ', ' ', ' ', ' '],
       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
        ' ', ' ', ' ', ' ', ' ', Style.BRIGHT + Fore.RED + '\\', Style.BRIGHT + Fore.RED + '=', Style.BRIGHT + Fore.RED + '=', Style.BRIGHT + Fore.RED + '\\', ' ',
        Style.BRIGHT + Fore.RED + '\\', Style.BRIGHT + Fore.RED + '|', Style.BRIGHT + Fore.RED + '\\', Style.BRIGHT + Fore.RED + '_', ' ', ' ', ' ', ' ', ' ', ' ',
        ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
        ' ', ' ', Style.BRIGHT + Fore.RED + '_', Style.BRIGHT + Fore.RED + '_', Style.BRIGHT + Fore.RED + '(', Style.BRIGHT + Fore.RED + '\\', Style.BRIGHT + Fore.RED + '=', Style.BRIGHT + Fore.RED + '=', Style.BRIGHT + Fore.RED + '=', Style.BRIGHT + Fore.RED + '\\',
        Style.BRIGHT + Fore.RED + '(', ' ', ' ', Style.BRIGHT + Fore.RED + ')', Style.BRIGHT + Fore.RED + '\\', ' ', ' ', ' ', ' ', ' ',
        ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
        ' ', Style.BRIGHT + Fore.RED + '(', Style.BRIGHT + Fore.RED + '(', Style.BRIGHT + Fore.RED + '(', Style.BRIGHT + Fore.RED + '~', Style.BRIGHT + Fore.RED + ')', ' ', Style.BRIGHT + Fore.RED + '_', Style.BRIGHT + Fore.RED + '_', Style.BRIGHT + Fore.RED + '(', Style.BRIGHT + Fore.RED + '_',
        Style.BRIGHT + Fore.RED + '/', ' ', ' ', ' ', Style.BRIGHT + Fore.RED + '|', ' ', ' ', ' ', ' ', ' ', ' ',
        ' ', ' ', ' ', ' ', ' ', ' '],
       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
        ' ', ' ', ' ', ' ', ' ', ' ', Style.BRIGHT + Fore.RED + '(', Style.BRIGHT + Fore.RED + '(', Style.BRIGHT + Fore.RED + '(', Style.BRIGHT + Fore.RED + '~', Style.BRIGHT + Fore.RED + ')',
        ' ', Style.BRIGHT + Fore.RED + '\\', ' ', ' ', Style.BRIGHT + Fore.RED + '/', ' ', ' ', ' ', ' ', ' ',
        ' ', ' ', ' ', ' ', ' ', ' ', ' '],
       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
        ' ', ' ', ' ', ' ', ' ', ' ', Style.BRIGHT + Fore.RED + '_', Style.BRIGHT + Fore.RED + '_', Style.BRIGHT + Fore.RED + '_', Style.BRIGHT + Fore.RED + '_', Style.BRIGHT + Fore.RED + '_',
        Style.BRIGHT + Fore.RED + '_', Style.BRIGHT + Fore.RED + '/', ' ', Style.BRIGHT + Fore.RED + '/', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
        ' ', ' ', ' ', ' ', ' ', ' '],
       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
        ' ', ' ', ' ', ' ', ' ', ' ', Style.BRIGHT + Fore.RED + "'", Style.BRIGHT + Fore.RED + '-', Style.BRIGHT + Fore.RED + '-', Style.BRIGHT + Fore.RED + '-', Style.BRIGHT + Fore.RED + '-',
        Style.BRIGHT + Fore.RED + '-', Style.BRIGHT + Fore.RED + '-', Style.BRIGHT + Fore.RED + "'", ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
        ' ', ' ', ' ', ' ', ' ', ' ']], dtype = 'object')
        
    def follow(self, obj):
        pos, size = obj.show()[0:2]

        obj_top = pos[0]
        obj_bottom = pos[0] + size[0]

        self_top = self.pos[0]
        self_bottom = self.pos[0] + self.size[0]

        if obj_top < self_top:
            self.pos[0] = obj_top

        if obj_bottom > self_bottom:
            self.pos[0] = obj_bottom - self.size[0]

    def take_hit(self):
        self.strength -= 1
        if self.strength <= 0:
            raise SystemExit

    def shoot(self, obj):
        return BossBullet(self.game_h, self.game_w, int(self.pos[0] + 7), int(self.pos[1] + 8), obj)