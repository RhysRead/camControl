#!/usr/bin/env python3

"""ImageRetrieval.py: Contains the code needed for retrieving and initially processing images
in the camControl project."""

__author__ = "Rhys Read"
__copyright__ = "Copyright 2018, Rhys Read"

import logging

import cv2


class Camera(object):
    def __init__(self):
        self.__cap = cv2.VideoCapture(0)

        if not self.__cap.isOpened():
            logging.fatal("Failed to open video capture feed. This is most likely the camera not being seen")

        self.__cap_x_size = self.__cap.get(3)
        self.__cap_y_size = self.__cap.get(4)

    def capture_image(self):
        ret, frame = self.__cap.read()
        return frame

    def close_feed(self):
        # todo: Complete this method
        pass