#!/usr/bin/env python3

"""Main.py: The main folder for the execution of the camControl project."""

__author__ = "Rhys Read"
__copyright__ = "Copyright 2018, Rhys Read"

import logging

from ImageRetrieval import Camera
from ImageProcessing import Image, ImageManager
from CursorProcessing import CursorManager

logging.basicConfig(level=logging.DEBUG)


class Main(object):
    def __init__(self):
        self.__video_feed = Camera()
        self.__image_manager = ImageManager()
        self.__cursor_manager = CursorManager(self.__video_feed.get_image_size())

    def start(self):
        # todo: Create this method.
        pass


if __name__ == "__main__":
    main = Main()
    main.start()
