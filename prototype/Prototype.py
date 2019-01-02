#!/usr/bin/env python3

"""Prototype.py: A mess of spaghetti code that I was prototyping with."""

__author__ = "Rhys Read"
__copyright__ = "Copyright 2018, Rhys Read"

import logging
import cv2
import pyautogui

pyautogui.FAILSAFE = False
logging.basicConfig(level=logging.INFO)

HAND_HAARCASCADE = "../haarcascades/hand.xml"


class Rectangle(object):
    def __init__(self, x, y, w, h):
        """
        Used to represent a rectangle and the co-ordinates of it's corners.
        :param x: The integer x value for the bottom left corner.
        :param y: The integer y value for the bottom left corner.
        :param w: The integer w value which can be added to the x value for the bottom right corner.
        :param h: The integer h value which can be added to the y value for the top left corner.
        """

        # Privately stores the co-ordinate values.
        self.__x = x
        self.__y = y
        self.__w = w
        self.__h = h

    def get_co_ordinates(self):
        """
        Returns the co-ordinates as a tuple.
        :return: The tuple (x, y, w, h,).
        """
        return self.__x, self.__y, self.__w, self.__h

    def get_pt1(self):
        """
        Get the bottom left point.
        :return: The tuple (x, y,)
        """
        return self.__x, self.__y

    def get_pt2(self):
        """
        Get the top right corner.
        :return: (x+w, y+h,)
        """
        return self.__x + self.__w, self.__y + self.__h


def get_hands(image, hand_template):
    """
    Used to detect the position of any hands present in an image using a haarcascade.
    :param image: OpenCV2 image object.
    :param hand_template: OpenCV2 haarcascade object.
    :return: A list of the hands in the image represented as a Rectangle object [Rectangle, Rectangle, ...].
    """
    # Applies the haarcascade to the image to find the hands
    detections = hand_template.detectMultiScale(image)

    # Iterates through the detections and converts them into Rectangle objects and appends them to a list
    hands = []
    for x, y, w, h in detections:
        hands.append(Rectangle(x, y, w, h))

    return hands


def draw_hands(image, hands):
    """
    Used to draw rectangles over an image where the hands are located.
    :param image: OpenCV2 image object.
    :param hands: List of Rectangle objects representing hand detections.
    :return: OpenCV2 image object.
    """
    # Return the unedited image if there are no hands to draw
    if hands is None:
        return image

    # Iterate through the hands and continue if a hand is None, otherwise get the hand co-ordinates and draw them
    #   on the image.
    for hand in hands:
        if hand is None:
            continue

        x, y, w, h = hand.get_co_ordinates()

        image = cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 1)

    # Return the image with the hands drawn over it
    return image


def find_biggest_hand(hands):
    """
    Used to find the biggest hand in a list of Rectangle objects representing hands.
    :param hands: A list of the hands in the image represented as a Rectangle object [Rectangle, Rectangle, ...].
    :return: A Rectangle object representing the largest hand in the list.
    """
    # Return None if no hands are passed to the function
    if hands is None or len(hands) < 1:
        return None

    # Iterate through the hands to find the largest hand
    largest_hand_so_far = hands[0]
    for hand in hands[1:]:
        # Get the co-ordinates for the two hands to compare
        x0, y0, w0, h0 = hand.get_co_ordinates()
        x1, y1, w1, h1 = largest_hand_so_far.get_co_ordinates()

        # Get the area of each of the hands
        size0 = w0 * h0
        size1 = w1 * h1

        # Set the new hand as the largest hand if it's area is greater than the current largest hand
        if size0 > size1:
            largest_hand_so_far = hand

    # Output that the hand was found and return it
    logging.debug("Found biggest hand.")
    return largest_hand_so_far


def move_cursor_with_ratio(hand, xratio, yratio):
    """
    Used to move the cursor to a position after applying the image to screen ratio to it.
    :param hand: Rectangle object representing a hand.
    :param xratio: Float ratio of image x axis to screen x axis.
    :param yratio: Float ratio of image y axis to screen y axis.
    :return: None.
    """
    # Return None if no hand is passed
    if hand is None:
        return

    # Extract co-ordinates from hand object
    x, y, w, h = hand.get_co_ordinates()

    # Apply the ratio to the co-ordinates to get the cursor position
    x_position = round(xratio * ((x + x) / 2))
    y_position = round(yratio * ((y + y) / 2))

    # Return none if the position is (0, 0)
    if x_position == 0.0 and y_position == 0.0:
        return

    # Output the cursor movement
    logging.debug("Moving cursor to: X={}, Y={}".format(x_position, y_position))

    # Move the cursor to the position
    pyautogui.moveTo(x_position, y_position)


if __name__ == "__main__":
    # Open a video capture feed
    cap = cv2.VideoCapture(0)

    # Output a fatal message if the video capture feed does not open
    if not cap.isOpened():
        logging.fatal("Failed to open video capture feed. This is most likely the camera not being seen")

    # Get the x and y size of the video capture feed
    cap_x_size = cap.get(3)
    cap_y_size = cap.get(4)

    # Get the x and y size of the screen
    screen_x_size, screen_y_size = pyautogui.size()

    # Create the image to screen ratios
    x_ratio = screen_x_size / cap_y_size
    y_ratio = screen_y_size / cap_y_size

    # Create the haarcascade used to detect hands
    hand_cascade = cv2.CascadeClassifier(HAND_HAARCASCADE)

    # Set cursor movement to True so that the cursor can be moved by the program
    move = True

    # Loop while the video capture feed is open
    while cap.isOpened():
        got_hands_multiple = []
        frame = None

        for i in range(0, 1):
            # Capture a video frame
            ret, frame = cap.read()
            # Flip the frame on the horizontal axis
            frame = cv2.flip(frame, 1)

            frame_average = frame

            # Get the modified versions of the image
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_blur = cv2.medianBlur(frame_gray, 5)
            frame_erode = cv2.erode(frame_blur, None,)

            # Get the hands from the image
            got_hands = get_hands(frame_blur, hand_cascade)
            got_hands_multiple.extend(got_hands)

            # Draw the hands on the image
            frame_hands = draw_hands(frame, got_hands)

            # Show the blurred image
            cv2.imshow("Blur", frame_blur)
            # cv2.imshow("Hands", frame_hands)

            # Wait for user key input
            value = cv2.waitKey(1)

            # Process user key input and respond accordingly
            if value == ord('q'):
                exit(0)
            elif value == ord('d'):
                logging.info("Paused cursor movement.")
                move = False
            elif value == ord('a'):
                logging.info("Enabled cursor movement.")
                move = True

        hands_average = got_hands_multiple

        # Find the biggest hand in the hands found
        biggest_hand = find_biggest_hand(hands_average)
        frame_average = draw_hands(frame, hands_average)

        if biggest_hand is not None:
            frame_average = cv2.rectangle(frame_average, biggest_hand.get_pt1(), biggest_hand.get_pt2(), (0, 255, 255), 2)

        cv2.imshow("Average", frame_average)
        if move:
            move_cursor_with_ratio(biggest_hand, x_ratio, y_ratio)
