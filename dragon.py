import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
import random
from time import monotonic as clock
import math

import config as conf
from thing import Thing


class Dragon(Thing):

    def __init__(self, game_height, game_width):

        x = game_height/2 - 3
        super().__init__(game_height, game_width, np.array([x, 0], dtype='float32'), np.array([6, 40]))

        self.vel = np.array([0, 0], dtype='float32')
        self.acc = np.array([conf.GRAVITY_X, conf.GRAVITY_Y])

        self.phase = 0
        self.big_count = 0
        self.fine_count = 0

        self.head = np.array([[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                            ['~', '~', '%', '%', 'z',
                                ' ', ' ', ' ', ' ', ' '],
                            ['~', '~', '~',
                                '(', 'O', 'O', ')', ' ', ' ', ' '],
                            ['~', '~', ' ', '*', '`', ':',
                                ':', '\\', '\\', ' '],
                            [' ', ' ', ' ', ' ', ' ',
                                ' ', ' ', '`', '@', '@'],
                            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']], dtype='object')

    def shift_up(self):
        temp = np.array([[' ' for j in range(self.head.shape[1])] for i in range(self.head.shape[0])], dtype='object')
        for i in range(1, self.head.shape[0]):
            temp[i - 1] = self.head[i]
        self.head = temp

    def shift_down(self):
        temp = np.array([[' ' for j in range(self.head.shape[1])] for i in range(self.head.shape[0])], dtype='object')
        for i in range(self.head.shape[0] - 1):
            temp[i + 1] = self.head[i]
        self.head = temp

    def nudge(self, key):
        if key == 'w':
            self.acc[0] -= conf.KEY_FORCE

    def reset_acc(self):
        super().reset_acc()
        self.acc[0] += conf.GRAVITY_X
        # self.acc[1] += conf.GRAVITY_Y


    def show(self):
        h = 6
        w = 30
        total_range = 2 * math.pi
        part = total_range / w

        input_arr = [(-math.pi + (i * part) + self.phase) for i in range(w)]
        sin_arr = np.sin(np.array(input_arr, dtype='float32')) * (3)

        dragon = np.array([[Style.BRIGHT + Fore.GREEN + '~' for j in range(w)]
                           for i in range(h)], dtype='object')

        for j in range(w):
            for i in range(min(0, int(round(sin_arr[j]))), max(0, int(round(sin_arr[j])))):
                dragon[i][j] = ' '

        dragon = np.concatenate((dragon, self.head), axis=1)

        self.phase += 0.5
        self.big_count += 1
        if self.big_count % 3 == 0:
            if self.fine_count % 4 == 0:
                self.shift_up()
            elif self.fine_count % 4 == 1:
                self.shift_down()
            elif self.fine_count % 4 == 2:
                self.shift_down()
            else:
                self.shift_up()
            self.fine_count += 1

        return np.round(self.pos).astype(np.int32), self.size, dragon

