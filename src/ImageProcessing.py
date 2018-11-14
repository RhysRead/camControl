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

    def get_hand_position(self):
        return self.__hand_postion

    def set_hand_position(self, position):
        self.__hand_postion = position


class ImageManager(object):
    def __init__(self, buffer_size=3):
        self.__buffer_size = buffer_size
        self.__buffer: [Image] = []

    def add_image(self, image: Image):
        image = process_image(image)

        if len(self.__buffer) == self.__buffer_size:
            self.__buffer.pop()

        self.__buffer.insert(0, image)

    def get_position(self):
        return self.__buffer[0].get_hand_position()

    def get_average_position(self):
        if len(self.__buffer) == 0:
            return None

        position = self.__buffer[0].get_hand_position()

        for hand in self.__buffer[1:]:
            position += hand.get_hand_position()

        return position / len(self.__buffer)


def get_hands(image: list):
    hands = hand_cascade.detectMultiScale(image)

    if hands is None:
        return

    return hands


def get_largest_hand(hands):
    if hands is None or len(hands) < 1:
        return None

    largest_hand_so_far = hands[0]
    for x0, y0, w0, h0 in hands[1:]:
        x1, y1, w1, h1 = largest_hand_so_far

        size0 = w0 * h0
        size1 = w1 * h1

        if size0 > size1:
            largest_hand_so_far = x0, y0, w0, h0

    return largest_hand_so_far


def get_hand_position(hand):
    x, y, w, h = hand
    # todo: Work out whether this works to get the centre of the hands position:
    return (x + x) / 2, (y + y) / 2,


def process_image(image: Image):
    gray_image = Image(image.gray_image())
    gray_blur_image = Image(image.blur_image())

    hands = get_hands(gray_blur_image.get_image())
    hand = get_largest_hand(hands)

    final_hand = Image(hand)

    return final_hand
