#!/usr/bin/env python3

"""PrecisionChecker.py: Purpose-built software to measure the accuracy of gesture tracking and cursor
control software."""

__author__ = "Rhys Read"
__copyright__ = "Copyright 2018, Rhys Read"

import logging

import tkinter as tk
import time
import pyautogui

TEST_TIME = 5.0
TEST_FREQUENCY = 0.1


class Interface(object):
    def __init__(self):
        """
        Interface used to host GUI and execute program.
        """
        self.tracker = AsyncTracker()

        self.__size: (int, int,) = None

        self.__root = tk.Tk()

        # Entry frame for entering data
        self.__entry_frame = tk.Frame(self.__root)

        # Title
        self.__entry_frame_label0 = tk.Label(self.__entry_frame,
                                             text='Please enter test parameters: ',
                                             font='Helvetica 18 bold',
                                             fg='Navy')
        self.__entry_frame_label0.grid(row=0, column=0)

        # Row 1
        self.__entry_frame_label1 = tk.Label(self.__entry_frame,
                                             text='Window X size: ',
                                             font='Helvetica 12',
                                             fg='Black')
        self.__entry_frame_label1.grid(row=1, column=0)

        self.__entry_frame_entry1 = tk.Entry(self.__entry_frame)
        self.__entry_frame_entry1.grid(row=1, column=1)

        # Row 2
        self.__entry_frame_label2 = tk.Label(self.__entry_frame,
                                             text='Window Y size: ',
                                             font='Helvetica 12',
                                             fg='Black')
        self.__entry_frame_label2.grid(row=2, column=0)

        self.__entry_frame_entry2 = tk.Entry(self.__entry_frame)
        self.__entry_frame_entry2.grid(row=2, column=1)

        # Row 3
        self.__entry_frame_label3 = tk.Label(self.__entry_frame,
                                             text='Minimum time: ',
                                             font='Helvetica 12',
                                             fg='Black')
        self.__entry_frame_label3.grid(row=3, column=0)

        self.__entry_frame_entry3 = tk.Entry(self.__entry_frame)
        self.__entry_frame_entry3.grid(row=3, column=1)

        # Row 4
        self.__entry_frame_button0 = tk.Button(self.__entry_frame,
                                               text='OK',
                                               font='Helvetica 16 bold',
                                               fg='Green',
                                               command=self.__begin_test)
        self.__entry_frame_button0.grid(row=4, column=1)

        # Frame is gridded here as it is the initial frame
        self.__entry_frame.grid()

        # Testing frame for actually running the test
        # Note that this is initialised later on due to sizing reasons
        self.__testing_frame = None

        self.__analysis_frame = tk.Frame(self.__root)
        self.__analysis_frame_label0 = tk.Label(self.__analysis_frame, text='', font='Helvetica 18 bold')
        self.__analysis_frame_label0.grid()

        self.__update()

    def __begin_test(self):
        """
        Method to begin test.
        :return:
        """
        # Entry frame is forgot as it is no longer needed
        self.__entry_frame.grid_forget()

        self.__size = (int(self.__entry_frame_entry1.get()), int(self.__entry_frame_entry2.get()),)

        # Testing frame is created according to parameters
        self.__testing_frame = tk.Frame(self.__root,
                                        width=self.__size[0],
                                        height=self.__size[1])
        # Testing frame is gridded as it is now needed
        self.__testing_frame.grid()
        self.__update()

        self.tracker.start()

        self.__testing_frame.after(int(TEST_TIME * 1000), func=self.__end_test)

    def __end_test(self):
        """
        Method to end test.
        :return:
        """
        result = self.tracker.get_results((self.__root.winfo_x(), self.__root.winfo_y(),),
                                          (self.__root.winfo_width(), self.__root.winfo_height(),))

        self.__analysis_frame_label0.config(text=str(result*100) + '% accuracy')

        self.__testing_frame.grid_forget()
        self.__analysis_frame.grid()

        self.__update()

    def __update(self):
        """
        Update the self.__root tk.Tk object.
        :return:
        """
        self.__root.update()

    def start(self):
        """
        Execute the program.
        :return:
        """
        self.__root.mainloop()


class AsyncTracker(object):
    def __init__(self):
        """
        Tracker used to asynchronously log cursor movement.
        """
        self.__results = []
        self.__complete = False

    def __log(self, duration: float, rate: float):
        start_time = time.time()
        while (time.time() - start_time) < duration:
            self.__results.append(tuple(pyautogui.position()))
            time.sleep(rate)

        self.__complete = True

    def get_results(self, window_position: (int, int,), window_size: (int, int,)):
        while not self.__complete:
            time.sleep(0.1)

        valid = 0
        for position in self.__results:
            if window_position[0] < position[0] < window_position[0] + window_size[0]:
                # Add 30 to Y value to account for Windows title bar. Note that this may be different on different machines.
                if window_position[1] + 30 < position[1] < window_position[1] + window_size[1] + 30:
                    valid += 1

        return valid/len(self.__results)

    def start(self):
        self.__log(TEST_TIME, TEST_FREQUENCY)


if __name__ == '__main__':
    tracker = Interface()
    tracker.start()
