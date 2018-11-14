#!/usr/bin/env python3

"""CursorProcessing.py: This file contains code that is used for processing
the cursor, screen axes, and general OS utilities."""

__author__ = "Rhys Read"
__copyright__ = "Copyright 2018, Rhys Read"

import pyautogui


def get_cursor_ratio(image_size: tuple, screen_size: tuple):
    x_ratio = screen_size[0] / image_size[0]
    y_ratio = screen_size[1] / image_size[1]

    return x_ratio, y_ratio


class CursorManager(object):
    def __init__(self, image_size: tuple):
        # todo: Check that the next line gets both the X and Y size. May need two variables.
        self.__screen_size = pyautogui.size()
        self.__ratio = get_cursor_ratio(image_size, self.__screen_size)

    def __execute_ratio(self, position: tuple):
        x = position[0] * self.__ratio[0]
        y = position[1] * self.__ratio[1]

        return x, y

    def move_cursor(self, unratioed_position: tuple):
        new_position = self.__execute_ratio(unratioed_position)

        pyautogui.position(new_position[0], new_position[1])

    def get_screen_size(self):
        return self.__screen_size
