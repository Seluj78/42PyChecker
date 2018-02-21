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
        self.chks = []
        for pick in picks:
            var = IntVar()
            chk = Checkbutton(self, text=pick, variable=var)
            chk.pack(side=side, anchor=anchor, expand=YES)
            self.chks.append(chk)
            self.vars.append(var)

    def state(self):
        return map((lambda var: var.get()), self.vars)


class Application:
    def __init__(self):
        self.path = None
        self.window = Tk()
        self.window.title("42PyChecker")
        self.window.minsize(width=800, height=800)
        self.options_dict = {'other': ['Author', 'Norme', 'Makefile'],
                              'libft': ['Author', 'Norme', 'Makefile','forbidden-functions', 'Static', 'Extra', 'Required', 'Bonus', 'Benchmark', 'Libftest', 'Maintest', 'Moulitest', 'libft-unit-test'],
                              'fillit': ['Author', 'Norme', 'Makefile', 'forbidden-functions', 'Fillit-Checker'],
                              '42commandements': []}
        # @todo: Make groups like when you tick `tests` it ticks all the tests


        # @todo: Set a icon for app image
        #self.window.iconbitmap(os.path.dirname(os.path.realpath(__file__)) + "/favicon.ico")



        # @todo: Find a way to loop through gif frames to have animated logo
        logo = PhotoImage(file=os.path.dirname(os.path.realpath(__file__)) + "/logo.gif")
        label = Label(self.window, image=logo)
        label.image = logo
        label.pack()


        Button(self.window, text="Select Project Path", width=20, command=self.get_project_path).pack()

        self.project = StringVar(self.window)
        self.project_name = None
        self.options = []
        self.project.trace("w", self.update_options)

        dropdown = OptionMenu(self.window, self.project, *self.options_dict.keys())
        dropdown.pack()

        self.options_choices = Checkbar(self.window, self.options)
        self.options_choices.pack(side=BOTTOM)

        Button(self.window, text="Exit", command=self.close_window).pack(side=BOTTOM)
        Button(self.window, text="Start", command=self.start).pack(side=BOTTOM)
        Button(self.window, text="Select All", command=self.select_all).pack(side=BOTTOM)
        Button(self.window, text="Deselect All", command=self.deselect_all).pack(side=BOTTOM)

        self.window.bind('<Escape>', self.close_window_escape)

    def select_all(self):
        for option in self.options_choices.chks:
            option.select()

    def deselect_all(self):
        for option in self.options_choices.chks:
            option.deselect()

    def close_window(self):
        self.window.destroy()
        sys.exit()

    def close_window_escape(self, event):
        self.window.destroy()
        sys.exit()

    def get_project_path(self):
        self.path = filedialog.askdirectory()

    def start(self):
        if not self.project_name:
            print("You need to select a project")
            return
        if not self.path:
            print("You need to select a path")
            return
        print(self.project_name)
        print(self.path)
        print(list(self.options_choices.state()))

    def update_options(self, *args):
        self.project_name = self.project.get()
        self.options = self.options_dict[self.project.get()]
        self.options_choices.destroy()
        self.options_choices = Checkbar(self.window, self.options)
        self.options_choices.pack(side=BOTTOM)

    def create_window(self):
        self.window.mainloop()
