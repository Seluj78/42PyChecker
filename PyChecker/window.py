"""
    Copyright (C) 2018 Jules Lasne <jules.lasne@gmail.com>
    See full notice in `LICENSE'
"""

from tkinter import *
import os
import sys
from tkinter import filedialog


class Checkbar(Frame):
    def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
        Frame.__init__(self, parent)
        self.vars = []
        for pick in picks:
            var = IntVar()
            chk = Checkbutton(self, text=pick, variable=var)
            chk.pack(side=side, anchor=anchor, expand=YES)
            self.vars.append(var)

    def state(self):
        return map((lambda var: var.get()), self.vars)


class Application():
    def __init__(self):
        self.window = Tk()
        self.window.title("42PyChecker")
        self.window.minsize(width=800, height=800)
        self.options_dict = {'other': ['author', 'norme', 'Makefile'],
                              'libft': ['author', 'forbidden-functions', 'makefile', 'norme', 'static', 'extra', 'required', 'bonus', 'benchmark', 'tests', 'libftest', 'maintest', 'moulitest', 'libft-unit-test'],
                              'fillit': ['author', 'forbidden-functions', 'makefile', 'norme', 'tests', 'fillit-checker'],
                              '42commandements': []}
        # @todo: Make groups like when you tick `tests` it ticks all the tests
        # @todo: Set a icon for app image
        #self.window.iconbitmap(os.path.dirname(os.path.realpath(__file__)) + "/favicon.ico")
        # @todo: Find a way to loop through gif frames to have animated logo
        logo = PhotoImage(file=os.path.dirname(os.path.realpath(__file__)) + "/logo.gif")
        Label(self.window, image=logo).pack()
        Button(self.window, text="Select Project Path", width=20, command=self.get_project_path).pack()
        self.project = StringVar(self.window)
        self.options = ['None', 'NULL']
        self.project.trace("w", self.update_options)
        dropdown = OptionMenu(self.window, self.project, *self.options_dict.keys())
        dropdown.pack()
        self.options_choices = Checkbar(self.window, self.options)
        self.options_choices.pack(side=BOTTOM)
        Button(self.window, text="Start", command=self.start).pack(side=BOTTOM)
        Button(self.window, text="Exit", command=self.close_window).pack(side=BOTTOM)
        self.window.bind('<Escape>', self.close_window_escape)

    def close_window(self):
        self.window.destroy()
        sys.exit()

    def close_window_escape(self, event):
        self.window.destroy()
        sys.exit()

    def get_project_path(self):
        self.path = filedialog.askdirectory()
        print(self.path)

    def start(self):
        print(list(self.options_choices.state()))

    def update_options(self, *args):
        self.options = self.options_dict[self.project.get()]
        self.options_choices.destroy()
        self.options_choices = Checkbar(self.window, self.options)
        self.options_choices.pack(side=BOTTOM)

    def create_window(self):
        self.window.mainloop()
