import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
import random

import config as conf

class Screen:

    CURSOR_0 = "\033[0;0H"

    def __init__(self, height, width):
        self._height = height
        self._width = width
        
        self._back_board = np.array([[conf.BG_COLOR for j in range(self._width)] for i in range(self._height)], dtype='object')
        for i in range(self._height):
            for j in range(self._width):
                # if (i + j) % 30 == 0 or (i - j) % 30 == 0:
                if random.random() < conf.ACCENT_AMT:
                    self._back_board[i][j] = conf.BG_ACCENT_COLOR

        for i in range(self._height - conf.GND_HEIGHT, self._height):
            for j in range(self._width):
                self._back_board[i][j] = conf.GND_COLOR

        for i in range(conf.SKY_DEPTH):
            for j in range(self._width):
                self._back_board[i][j] = conf.SKY_COLOR

        self._fore_board = np.array([[' ' for j in range(self._width)] for i in range(self._height)], dtype='object')

    def clear(self):
        # for i in range(self._height):
        #     for j in range(self._width):
        #         if random.random() < conf.ACCENT_AMT:
        #             self._back_board[i][j] = conf.BG_ACCENT_COLOR
        #         else:
        #             self._back_board[i][j] = conf.BG_COLOR
        
        # for i in range(self._height - conf.GND_HEIGHT, self._height):
        #     for j in range(self._width):
        #         self._back_board[i][j] = conf.GND_COLOR

        # for i in range(conf.SKY_DEPTH):
        #     for j in range(self._width):
        #         self._back_board[i][j] = conf.SKY_COLOR

        for i in range(self._height):
            for j in range(self._width):
                self._fore_board[i][j] = ' '

    def add(self, obj):
        if True in obj.is_out():
            return

        pos, size, front = obj.show()
        
        x_start = pos[0]
        x_start_ = 0
        x_end = pos[0] + size[0]
        x_end_ = size[0]
        y_start = pos[1]
        y_start_ = 0
        y_end = pos[1] + size[1]
        y_end_ = size[1]

        # Now make sure if half the object is visible, it is rendered correctly

        if x_start < 0:
            x_start_ = 0 - x_start
            x_start = 0

        if y_start < 0:
            y_start_ = 0 - y_start
            y_start = 0

        if x_end > self._height:
            x_end_ = self._height - pos[0]
            x_end = self._height

        if y_end > self._width:
            y_end_ = self._width - pos[1]
            y_end = self._width

        try:
            self._fore_board[x_start:x_end, y_start:y_end] = front[x_start_:x_end_, y_start_:y_end_]
        except (IndexError, ValueError) as e:
            return

    def print_board(self):
        print(self.CURSOR_0)
        for i in range(self._height):
            for j in range(self._width):
                print(self._back_board[i][j] + self._fore_board[i][j], end='')
            print('')
