#!/usr/bin/env python3

"""ImageProcessing.py: This file contains code that is used for processing
images that are passed to it.."""

__author__ = "Rhys Read"
__copyright__ = "Copyright 2018, Rhys Read"

import logging

import cv2

HAND_HAARCASCADE = "../haarcascades/hand.xml"
hand_cascade = cv2.CascadeClassifier(HAND_HAARCASCADE)


class Image(object):
    def __init__(self, image: list):
        self.__image = image
        self.__hand_postion = None

    def gray_image(self):
        return cv2.cvtColor(self.__image, cv2.COLOR_BGR2GRAY)

    def blur_image(self):
        return cv2.medianBlur(self.__image, 5)

    def erode_image(self):
        return cv2.erode(self.__image, None)

    def get_image(self):
        return self.__image

    def set_hand_position(self, position):
        self.__hand_postion = position


class ImageManager(object):
    def __init__(self, buffer_size=3):
        self.__buffer_size = buffer_size
        self.__buffer = []

    def add_image(self, image: Image):
        if len(self.__buffer) > self.__buffer_size:
            self.__buffer.pop()
        self.__buffer.insert(0, image)


def get_hand_position(image):
    found =