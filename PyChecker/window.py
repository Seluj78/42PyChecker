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

    def close_window(self):
        self.window.destroy()
        sys.exit()

    def close_window_escape(self, event):
        self.window.destroy()
        sys.exit()

    def get_project_path(self):
        self.path = filedialog.askdirectory()
        print(self.path)

    def callback_project_name_changed(self, *args):
        # @todo: Make groups like when you tick `tests` it ticks all the tests
        self.project_selected = self.project.get()
        if self.project_selected == "other":
            # @todo: whitelist/blacklist for options
            self.options = Checkbar(self.window, ['author', 'norme', 'Makefile'])
            self.options.pack(side=LEFT)

        if self.project_selected == "42commandements":
            self.options = None

        if self.project_selected == "libft":
            self.options = Checkbar(self.window, ['author', 'forbidden-functions', 'makefile', 'norme', 'static', 'extra', 'required', 'bonus', 'benchmark', 'tests', 'libftest', 'maintest', 'moulitest', 'fillit-checker', 'libft-unit-test'])
            self.options.pack(side=LEFT)

        if self.project_selected == "fillit":
            self.options = Checkbar(self.window, ['author', 'forbidden-functions', 'makefile', 'norme', 'tests', 'fillit-checker'])
            self.options.pack(side=LEFT)

    def start(self):
        if self.options != None:
            print(list(self.options.state()))

    def create_window(self):
        self.window.title("42PyChecker")
        self.window.minsize(width=800, height=800)
        # @todo: Set a icon for app image
        #self.window.iconbitmap(os.path.dirname(os.path.realpath(__file__)) + "/favicon.ico")
        # @todo: Find a way to loop through gif frames to have animated logo
        logo = PhotoImage(file=os.path.dirname(os.path.realpath(__file__)) + "/logo.gif")
        Label(self.window, image=logo).pack()
        Button(self.window, text="Select Project Path", width=20, command=self.get_project_path).pack()

        self.project = StringVar(self.window)
        dropdown = OptionMenu(self.window, self.project, "other", "42commandements", "libft", 'fillit')
        dropdown.pack()

        Button(self.window, text="Start", command=self.start).pack(side=BOTTOM)

        Button(self.window, text="Exit", command=self.close_window).pack(side=BOTTOM)
        self.window.bind('<Escape>', self.close_window_escape)

        self.project.trace("w", self.callback_project_name_changed)
        self.window.mainloop()
