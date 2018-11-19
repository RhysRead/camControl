#!/usr/bin/env python3

"""Main.py: The main folder for the execution of the camControl project."""

__author__ = "Rhys Read"
__copyright__ = "Copyright 2018, Rhys Read"

import logging

from ImageRetrieval import Camera
from ImageProcessing import Image, ImageManager
from CursorProcessing import CursorManager
from UserInterface import InterfaceManager

logging.basicConfig(level=logging.DEBUG)


class Main(object):
    def __init__(self):
        self.__video_feed = Camera()
        self.__image_manager = ImageManager()
        self.__cursor_manager = CursorManager(self.__video_feed.get_image_size())
        self.__interface_manager = InterfaceManager(self.__cursor_manager)

    def start(self):
        while True:
            frame = self.__video_feed.capture_image()

            self.__image_manager.add_image(frame)
            position = self.__image_manager.get_average_position()
            self.__cursor_manager.move_cursor(position)

        # Stop procedure:
        self.__video_feed.close_feed()


if __name__ == "__main__":
    main = Main()
    main.start()
