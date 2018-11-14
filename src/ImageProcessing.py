#!/usr/bin/env python3

"""ImageProcessing.py: This file contains code that is used for processing
images that are passed to it.."""

__author__ = "Rhys Read"
__copyright__ = "Copyright 2018, Rhys Read"

import logging

import cv2

HAND_HAARCASCADE = "../haarcascades/hand.xml"


class Image(object):
    def __init__(self, image):
        self.__image = image

    def gray_image(self):
        return cv2.cvtColor(self.__image, cv2.COLOR_BGR2GRAY)

    def blur_image(self):
        return cv2.medianBlur(self.__image, 5)

    def erode_image(self):
        return cv2.erode(self.__image, None)

    def get_image(self):
        return self.__image


class ImageManager(object):
    def __init__(self, buffer_size=3):
        self.__buffer_size = buffer_size
        self.__buffer = []

    def add_image(self, image):
        if len(self.__buffer) > self.__buffer_size:
            self.__buffer.pop()
        self.__buffer.insert(0, image)
    
