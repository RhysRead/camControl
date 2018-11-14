#!/usr/bin/env python3

"""Main.py: The main folder for the execution of the camControl project."""

__author__ = "Rhys Read"
__copyright__ = "Copyright 2018, Rhys Read"

import logging

from ImageRetrieval import Camera

logging.basicConfig(level=logging.DEBUG)


class Main(object):
    def __init__(self):
        self.__video_feed = Camera()

    def start(self):
        # todo: Create this method.
        pass


if __name__ == "__main__":
    main = Main()
