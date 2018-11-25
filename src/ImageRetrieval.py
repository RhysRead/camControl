#!/usr/bin/env python3

"""ImageRetrieval.py: Contains the code needed for retrieving and initially processing images
in the camControl project."""

__author__ = "Rhys Read"
__copyright__ = "Copyright 2018, Rhys Read"

import logging

import cv2


class Camera(object):
    def __init__(self):
        """
        The Camera object is used to maintain the video feed to capture web-cam images.
        """
        self.__cap = cv2.VideoCapture(0)

        if not self.__cap.isOpened():
            logging.fatal("Failed to open video capture feed. This is most likely the camera not being seen")

        self.__cap_x_size = self.__cap.get(3)
        self.__cap_y_size = self.__cap.get(4)

    def capture_image(self):
        """
        Capture an image from the video feed.
        :return: OpenCV2 image from video feed.
        """
        ret, frame = self.__cap.read()
        return frame

    def get_image_size(self):
        """
        Get the image size of the images from this video feed.
        :return: (x, y, ) for the size of the images from this video feed.
        """
        return self.__cap_x_size, self.__cap_y_size

    def close_feed(self):
        """
        Close down the video feed.
        :return None:
        """
        # todo: Complete this method
        pass
