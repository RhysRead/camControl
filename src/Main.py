#!/usr/bin/env python3

"""Main.py: The main folder for the execution of the camControl project."""

__author__ = "Rhys Read"
__copyright__ = "Copyright 2018, Rhys Read"

import logging

from ImageRetrieval import Camera
from ImageProcessing import Image, ImageManager
from CursorProcessing import CursorManager
from UserInterface import InterfaceManager

from cv2 import imshow

logging.basicConfig(level=logging.DEBUG)


class Main(object):
    def __init__(self):
        self.__video_feed = Camera()
        self.__image_manager = ImageManager()
        self.__cursor_manager = CursorManager(self.__video_feed.get_image_size())
        self.__interface_manager = InterfaceManager(self.__cursor_manager)

    def start(self):
        """
        Used to execute the main loop of camControl.
        :return None:
        """
        # Main loop
        while True:
            # Capture image from video feed
            frame = self.__video_feed.capture_image()

            # Log and process the image
            self.__image_manager.add_image(frame)
            position = self.__image_manager.get_average_position()

            # Move the cursor if a valid position is found
            if position is not None:
                self.__cursor_manager.move_cursor(position)

            # Present the un-edited image to the user
            imshow("Video", frame)

            # Get the user input
            user_input = self.__interface_manager.get_user_input()

            # Quit if the user selected the exit key
            if user_input == 1:
                break

        # Stop procedure:
        self.__video_feed.close_feed()


# Execute main loop if Main.py is executed as the main thread
if __name__ == "__main__":
    main = Main()
    main.start()
