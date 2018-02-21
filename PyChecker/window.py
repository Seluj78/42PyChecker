"""
    Copyright (C) 2018 Jules Lasne <jules.lasne@gmail.com>
    See full notice in `LICENSE'
"""

from tkinter import *
import os
import sys
from tkinter import filedialog
from tkinter import messagebox

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
        self.root_path = os.path.dirname(os.path.realpath(__file__))
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

            # @todo: Display path somewhere when selected
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


        self.main_menu = Menu(self.window)

        self.about_menu = Menu(self.main_menu)
        self.about_menu.add_command(label="About", command=self.display_about)
        self.about_menu.add_command(label="Warranty", command=self.display_warranty)
        self.about_menu.add_command(label="License", command=self.display_license)

        self.main_menu.add_cascade(label="About", menu=self.about_menu)

        self.window.config(menu=self.main_menu)
        self.window.bind('<Escape>', self.close_window_escape)

    def display_about(self):
        msg = "\t42PyChecker  Copyright (C) 2018-present Jules Lasne " \
              "<jules.lasne@gmail.com>\n\tThis program comes with ABSOLUTELY " \
              "NO WARRANTY; for details run with `--show-w'.\n\tThis is free " \
              "software, and you are welcome to redistribute it\n\tunder " \
              "certain conditions; run with `--show-c' for details."
        popup = Tk()
        popup.wm_title("About")
        label = Label(popup, text=msg)
        label.pack(side="top", fill="x", pady=10)
        B1 = Button(popup, text="Okay", command=popup.destroy)
        B1.pack()
        popup.mainloop()

    def display_warranty(self):
        msg = "THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED" \
              " BY APPLICABLE LAW. EXCEPT WHEN OTHERWISE STATED IN WRITING\n" \
              " THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM" \
              " “AS IS” WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR\n" \
              " IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES" \
              " OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE\n" \
              " ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS" \
              " WITH YOU. SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME\n" \
              " THE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION."
        popup = Tk()
        popup.wm_title("Warranty Statement")
        label = Label(popup, text=msg)
        label.pack(side="top", fill="x", pady=10)
        B1 = Button(popup, text="Okay", command=popup.destroy)
        B1.pack()
        popup.mainloop()

    def display_license(self):
        popup = Tk()
        popup.wm_title("License")
        with open(self.root_path + '/../.github/LICENSE.lesser', 'r') as file:
            filedata = file.read()
        txt = Text(popup, borderwidth=3, relief="sunken")
        txt.insert(END, filedata)
        txt.config(font=("consolas", 12), undo=True, wrap='word')
        txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        scrollb = Scrollbar(popup, command=txt.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        txt['yscrollcommand'] = scrollb.set
        B1 = Button(popup, text="Okay", command=popup.destroy)
        B1.grid()
        popup.mainloop()

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
            messagebox.showerror("Project not specified", "You need to specify the project you want to test.")
            return
        if not self.path:
            messagebox.showerror("Path not specified", "You need to specify the path of the project you want to test.")
            return
        # @todo: Can't select 42commandements because of this. Need workaround
        has_selected = 0
        for choice in self.options_choices.state():
            if choice == 1:
                has_selected = 1
                break
        if not has_selected:
            messagebox.showwarning("No options", "You havent selected any options.")
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
