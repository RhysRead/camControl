#!/usr/bin/env python3

"""UserInterface.py: Contains the code needed for managing the camControl user interface."""

__author__ = "Rhys Read"
__copyright__ = "Copyright 2018, Rhys Read"

import logging

import cv2


class InterfaceManager(object):
    def __init__(self, cursor_manager):
        self.__windows = {}
        self.__cursor_manager = cursor_manager

    def get_user_input(self):
        """
        Used to retrieve and handle the user input.
        :return: The code relevant to the user input.
        """
        # Use opencv2 to get the user's input
        value = cv2.waitKey(1)

        # Handle the user's input
        if value == ord('q'):
            # Return 1 if exit button is pressed.
            return 1
        elif value == ord('d'):
            logging.info("Paused cursor movement.")
            self.__cursor_manager.disable()
            # Return 2 if cursor pause button is pressed.
            return 2
        elif value == ord('a'):
            logging.info("Enabled cursor movement.")
            self.__cursor_manager.enable()
            # Return 3 if cursor enable button is pressed.
            return 3

        # Return 0 if no user input is found.
        return 0
