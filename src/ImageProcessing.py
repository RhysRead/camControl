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
        """
        Object used to represent an image.
        :param image: OpenCV2 image.
        """
        self.__image = image
        self.__hand_postion = None

    def gray_image(self):
        """
        Used to get the gray version of the object's stored image.
        :return: Gray version of the object's stored image.
        """
        return cv2.cvtColor(self.__image, cv2.COLOR_BGR2GRAY)

    def blur_image(self):
        """
        Used to get the blurred version of the object's stored image.
        :return: Blurred version of the object's stored image.
        """
        return cv2.medianBlur(self.__image, 5)

    def erode_image(self):
        """
        Used to get the eroded version of the object's stored image.
        :return: Eroded version of the object's stored image.
        """
        return cv2.erode(self.__image, None)

    def get_image(self):
        """
        Used to get the original version of the object's stored image.
        :return: Original version of the object's stored image.
        """
        return self.__image

    def get_hand_position(self):
        """
        Used to get the hand position associated with the stored image.
        :return: The hand position associated with the stored image.
        """
        return self.__hand_postion

    def set_hand_position(self, position):
        """
        Used to set the hand position associated with the stored image.
        :param position: The hand position associated with the stored image.
        :return None:
        """
        self.__hand_postion = position


class ImageManager(object):
    def __init__(self, buffer_size=3):
        """
        The ImageManager object is used to manage the saved images and handle the process of creating movement
        patterns for the camControl software.
        :param buffer_size: The amount of consecutive images and their hand positions to store.
        """
        self.__buffer_size = buffer_size
        self.__buffer: [Image] = []

    def add_image(self, image: Image):
        """
        Add and image to the image buffer.
        :param image: Image object to be added to the buffer.
        :return None:
        """
        image = process_image(image)

        if image is None:
            return

        if len(self.__buffer) == self.__buffer_size:
            self.__buffer.pop()

        self.__buffer.insert(0, image)

    def get_position(self):
        """
        Get the position of the most recently appended image.
        :return: The position of the most recently appended image.
        """
        return self.__buffer[0].get_hand_position()

    def get_average_position(self):
        """
        Get the average position of the hand across the logged buffer permissions.
        :return: The average position of the hand across the logged buffer permissions.
        """
        if len(self.__buffer) == 0 or self.__buffer[0] is None:
            return None

        position = list(self.__buffer[0].get_hand_position())

        if position is None:
            return None

        mean_count = 1
        for hand in self.__buffer[1:]:
            if hand is None:
                continue
            mean_count += 1
            position[0] += hand.get_hand_position()[0]
            position[1] += hand.get_hand_position()[1]

        return tuple([i / mean_count for i in position])


def get_hands(image: list):
    """
    Detect the hands in an OpenCV2 image and return them.
    :param image: An OpenCV2 image.
    :return: The hands found in the image given.
    """
    hands = hand_cascade.detectMultiScale(image)

    if hands is None:
        return None

    return hands


def get_largest_hand(hands):
    """
    Iterate through a list of hands found in an image and return the largest hand found.
    :param hands: A list of hands found in an image.
    :return: The largest hand found.
    """
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
    """
    Gets the position of a hand found.
    :param hand: A hand found by the hand haarcascade.
    :return: (x, y,) representing the centre position of the hand provided.
    """
    x, y, w, h = hand
    # todo: Work out whether this works to get the centre of the hands position: Pretty sure it does but test more
    return (x + x) / 2, (y + y) / 2,


def process_image(image: Image):
    """
    Used to handle a large chunk of the processing of an image to return an Image object of the largest hand in an image
    :param image: Image object containing the image you desire to be processed.
    :return: Image object containing the largest hand found in the original image.
    """
    gray_image = Image(image.gray_image())
    gray_blur_image = Image(gray_image.blur_image())

    hands = get_hands(gray_blur_image.get_image())
    largest_hand = get_largest_hand(hands)
    if largest_hand is None:
        return None
    largest_hand_image = Image(list(largest_hand))
    largest_hand_image.set_hand_position((largest_hand[0], largest_hand[1],))

    return largest_hand_image
