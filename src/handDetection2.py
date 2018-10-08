# Rhys Read
# Test

import logging
import cv2
import pyautogui

pyautogui.FAILSAFE = False
logging.basicConfig(level=logging.INFO)

HAND_HAARCASCADE = "../haarcascades/hand.xml"


class Rectangle(object):
    def __init__(self, x, y, w, h):

        self.__x = x
        self.__y = y
        self.__w = w
        self.__h = h

    def get_co_ordinates(self):
        return self.__x, self.__y, self.__w, self.__h

    def get_pt1(self):
        return self.__x, self.__y

    def get_pt2(self):
        return self.__x + self.__w, self.__y + self.__h


def get_hands(image, hand_template):
    detections = hand_template.detectMultiScale(image)

    hands = []
    for x, y, w, h in detections:
        hands.append(Rectangle(x, y, w, h))

    return hands


def draw_hands(image, hands):
    if hands is None:
        return image

    for hand in hands:
        if hand is None:
            continue

        x, y, w, h = hand.get_co_ordinates()

        image = cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 1)

    return image


def union(a, b):
    x = min(a[0], b[0])
    y = min(a[1], b[1])
    w = max(a[0]+a[2], b[0]+b[2]) - x
    h = max(a[1]+a[3], b[1]+b[3]) - y
    return x, y, w, h


def intersection(a, b):
    x = max(a[0], b[0])
    y = max(a[1], b[1])
    w = min(a[0]+a[2], b[0]+b[2]) - x
    h = min(a[1]+a[3], b[1]+b[3]) - y
    if w < 0 or h < 0:
        return ()  # or (0,0,0,0) ?
    return x, y, w, h


def find_biggest_hand(hands):
    if hands is None or len(hands) < 1:
        return None

    largest_hand_so_far = hands[0]
    for hand in hands[1:]:
        x0, y0, w0, h0 = hand.get_co_ordinates()
        x1, y1, w1, h1 = largest_hand_so_far.get_co_ordinates()

        size0 = w0 * h0
        size1 = w1 * h1

        if size0 > size1:
            largest_hand_so_far = hand

    logging.debug("Found biggest hand.")
    return largest_hand_so_far


def move_cursor_with_ratio(hand, xratio, yratio):
    if hand is None:
        return

    x, y, w, h = hand.get_co_ordinates()

    x_position = round(xratio * ((x + x) / 2))
    y_position = round(yratio * ((y + y) / 2))

    if x_position == 0.0 and y_position == 0.0:
        return

    logging.debug("Moving cursor to: X={}, Y={}".format(x_position, y_position))

    pyautogui.moveTo(x_position, y_position)


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    cap_x_size = cap.get(3)
    cap_y_size = cap.get(4)

    screen_x_size, screen_y_size = pyautogui.size()

    if cap_y_size != 0:
        logging.WARNING("Failed to generate cursor ratios.")
        x_ratio = screen_x_size / cap_y_size
        y_ratio = screen_y_size / cap_y_size

    hand_cascade = cv2.CascadeClassifier(HAND_HAARCASCADE)

    move = True

    if not cap.isOpened():
        logging.fatal("Failed to open video capture feed. This is most likely the camera not being seen")

    while cap.isOpened():
        got_hands_multiple = []
        frame = None

        for i in range(0, 1):
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)

            frame_average = frame

            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_blur = cv2.medianBlur(frame_gray, 5)
            frame_erode = cv2.erode(frame_blur, None,)

            got_hands = get_hands(frame_blur, hand_cascade)
            got_hands_multiple.extend(got_hands)

            frame_hands = draw_hands(frame, got_hands)

            cv2.imshow("Blur", frame_blur)
            # cv2.imshow("Hands", frame_hands)

            value = cv2.waitKey(1)

            if value == ord('q'):
                exit(0)
            elif value == ord('d'):
                logging.info("Paused cursor movement.")
                move = False
            elif value == ord('a'):
                logging.info("Enabled cursor movement.")
                move = True

        hands_average = got_hands_multiple

        biggest_hand = find_biggest_hand(hands_average)
        frame_average = draw_hands(frame, hands_average)

        if biggest_hand is not None:
            frame_average = cv2.rectangle(frame_average, biggest_hand.get_pt1(), biggest_hand.get_pt2(), (0, 255, 255), 2)

        cv2.imshow("Average", frame_average)
        if move:
            move_cursor_with_ratio(biggest_hand, x_ratio, y_ratio)
