#!/usr/bin/env python3

"""Main.py: The main folder for the execution of the camControl project."""

__author__ = "Rhys Read"
__copyright__ = "Copyright 2018, Rhys Read"

import logging

from ImageRetrieval import Camera
from ImageProcessing import Image, ImageManager
from CursorProcessing import CursorManager
from UserInterface import InterfaceManager
from Database import DataBaseManager

from cv2 import imshow, rectangle, flip

logging.basicConfig(level=logging.DEBUG)


class Main(object):
    def __init__(self):
        # Create Camera object to act as the video feed
        self.__video_feed = Camera()
        # Create manager objects to control and manage the program.
        self.__image_manager = ImageManager()
        # Get image size from video feed
        image_size = self.__video_feed.get_image_size()
        # If image size is 0 then the webcam is not connected, hence halt the program
        if image_size[0] or image_size[1] == 0:
            logging.error('Please connect a valid USB webcam.')
            exit(1)
        self.__cursor_manager = CursorManager(image_size)
        self.__interface_manager = InterfaceManager(self.__cursor_manager)
        self.__database_manager = DataBaseManager()

    def start(self):
        """
        Used to execute the main loop of camControl.
        :return None:
        """
        # Creates a session and gets the session key
        session_key = self.__database_manager.create_session()
        # Main loop
        while True:
            # Capture image from video feed
            frame = self.__video_feed.capture_image()

            # Flip the image on the horizontal axis
            frame = flip(frame, 1)

            # Log and process the image
            self.__image_manager.add_image(Image(frame))
            position = self.__image_manager.get_average_position()

            # Move the cursor if a valid position is found
            if position is not None:
                # Log the cursor movement to the database
                self.__database_manager.store_cursor(position, session_key)
                # Execute the cursor movement to the position found
                self.__cursor_manager.move_cursor(position)
                # Get the rounded integer value for the cursor position as a tuple
                xy = (int(round(position[0])), int(round(position[1])),)
                # Draw a dot over the image to represent where the hand has been seen
                edited_image = rectangle(frame, xy, xy, (0, 255, 0,), 20)

                # Present the un-edited image to the user
                imshow("Video", edited_image)

            # Get the user input
            user_input = self.__interface_manager.get_user_input()

            # Quit if the user selected the exit key
            if user_input == 1:
                break

        # Stop procedure:
        self.__video_feed.close_feed()
        self.__database_manager.end_session(session_key)
        self.__database_manager.save_changes()


# Execute main loop if Main.py is executed as the main thread
if __name__ == "__main__":
    main = Main()
    main.start()
