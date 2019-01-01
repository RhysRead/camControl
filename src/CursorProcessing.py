#!/usr/bin/env python3

"""CursorProcessing.py: This file contains code that is used for processing
the cursor, screen axes, and general OS utilities."""

__author__ = "Rhys Read"
__copyright__ = "Copyright 2018, Rhys Read"

import pyautogui
import threading


def get_cursor_ratio(image_size: tuple, screen_size: tuple):
    """
    Used to calculate the ratio of the x and y axis of the image to the screen size.
    :param image_size: (x, y,) of image size.
    :param screen_size: (x, y,) of screen size.
    :return: (x, y,) as the ratio of the image size to the screen size.
    """
    x_ratio = screen_size[0] / image_size[0]
    y_ratio = screen_size[1] / image_size[1]

    return x_ratio, y_ratio


class CursorManager(object):
    def __init__(self, image_size: tuple):
        """
        CursorManager is used to manipulate the cursor and manage the processes which control the computer.
        :param image_size: (x, y,) of the size of images being used.
        """
        # todo: Check that the next line gets both the X and Y size. May need two variables.
        self.__screen_size = pyautogui.size()
        self.__ratio = get_cursor_ratio(image_size, self.__screen_size)

        self.__enabled = True

    def __execute_ratio(self, position: tuple):
        """
        Calculates the position given when multiplied by the image to screen ratio.
        :param position: (x, y,) of the position to move the cursor to.
        :return: (x, y,) of the new position after being multiplied by the ratio.
        """
        x = position[0] * self.__ratio[0]
        y = position[1] * self.__ratio[1]

        return x, y

    def move_cursor(self, unratioed_position: tuple):
        """
        Used to move the cursor to the new position. Calculates the ratio automatically.
        :param unratioed_position: (x, y,) the unratioed position to move the cursor to.
        :return: None
        """
        if self.__enabled is False:
            return

        # Apply the previously calculated ratio to the hand position to move the cursor to the appropriate position
        new_position = self.__execute_ratio(unratioed_position)

        # Create a separate thread to move the cursor over a period of time to avoid hanging the program
        t = threading.Thread(target=async_move, args=(new_position, 0.1))
        t.start()

    def get_screen_size(self):
        """
        Used to get the screen resolution/size.
        :return: (x, y,) of the screen size
        """
        return self.__screen_size

    def enable(self):
        """
        Enables cursor movement.
        :return None:
        """
        self.__enabled = True

    def disable(self):
        """
        Disables cursor movement.
        :return None:
        """
        self.__enabled = False


def async_move(position: tuple, time: float):
    """
    Method to asynchronously move the cursor to a position of a period of time.
    :param position: The tuple (x, y,) position you desire to move the cursor to.
    :param time: The float value for the time you would like the cursor to take to assume the new position.
    :return: None
    """
    pyautogui.moveTo(position[0], position[1], time)
