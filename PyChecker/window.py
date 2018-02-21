"""
    Copyright (C) 2018 Jules Lasne <jules.lasne@gmail.com>
    See full notice in `LICENSE'
"""

from tkinter import *
import os
import sys
from tkinter import filedialog
from tkinter import messagebox
import logging
from PyChecker.projects import libft, ft_commandements, other, fillit


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


class Application():
    def __init__(self, args):
        self.root_path = os.path.dirname(os.path.realpath(__file__))
        self.path = None
        self.args = args

        # Create the window instance and set a few parameters
        logging.info("Initializing window")
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

        # Sets the logo image on top
        # @todo: Move logo into special folder
        logging.debug("Adding logo to window")
        logo = PhotoImage(file=os.path.dirname(os.path.realpath(__file__)) + "/logo.gif")
        label = Label(self.window, image=logo)
        label.image = logo
        label.pack()

        # @todo: Display path somewhere when selected
        # Creates a button
        logging.debug("Adding `project path` button")
        Button(self.window, text="Select Project Path", width=20, command=self.get_project_path).pack()

        # Creates variables and starts a tracer on variable
        self.project = StringVar(self.window)
        self.project_name = None
        self.options = []
        self.project.trace("w", self.update_options)

        # Creates dropdown menu with project options
        logging.debug("Adding DropDown menu for projects")
        dropdown = OptionMenu(self.window, self.project, *self.options_dict.keys())
        dropdown.config(width=len("42commandements"))
        dropdown.pack()

        # Creates a checkbar based on choice made with the optionmenu
        logging.debug("Adding checkboxes ")
        self.options_choices = Checkbar(self.window, self.options)
        self.options_choices.pack(side=BOTTOM)

        # Creates buttons
        logging.debug("Adding buttons")
        Button(self.window, text="Exit", command=self.close_window).pack(side=BOTTOM)
        Button(self.window, text="Start", command=self.start).pack(side=BOTTOM)
        Button(self.window, text="Select All", command=self.select_all).pack(side=BOTTOM)
        Button(self.window, text="Deselect All", command=self.deselect_all).pack(side=BOTTOM)

        # Creates a menu
        # @todo: Add a menu option to display log
        logging.debug("Adding menu")
        self.main_menu = Menu(self.window)
        self.about_menu = Menu(self.main_menu)
        self.about_menu.add_command(label="About", command=self.display_about)
        self.about_menu.add_command(label="Warranty", command=self.display_warranty)
        self.about_menu.add_command(label="License", command=self.display_license)
        self.main_menu.add_cascade(label="About", menu=self.about_menu)
        self.window.config(menu=self.main_menu)

        # Binds the escape key with closing the program
        self.window.bind('<Escape>', self.close_window_escape)
        logging.info("Creating Window")
        self.window.mainloop()

    def display_about(self):
        """
        Creates a popup to display the about.
        """
        logging.debug("Creating About pop-up")
        msg = "\t42PyChecker  Copyright (C) 2018-present Jules Lasne " \
              "<jules.lasne@gmail.com>\n\tThis program comes with ABSOLUTELY " \
              "NO WARRANTY; for details open menu About->Warranty.\n\tThis is free " \
              "software, and you are welcome to redistribute it\n\tunder " \
              "certain conditions; Open menu About->License for details."
        popup = Tk()
        popup.wm_title("About")
        Label(popup, text=msg).pack(side="top", fill="x", pady=10)
        Button(popup, text="Okay", command=popup.destroy).pack()
        popup.mainloop()

    def display_warranty(self):
        """
        Creates a popup to display the warranty
        """
        logging.debug("Creating warranty pop-up")
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
        Label(popup, text=msg).pack(side="top", fill="x", pady=10)
        Button(popup, text="Okay", command=popup.destroy).pack()
        popup.mainloop()

    def display_license(self):
        """
        Creates a popup and displays the file LICENSE.lesser inside of it.
        """
        logging.debug("Creating License pop-up")
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
        Button(popup, text="Okay", command=popup.destroy).grid()
        popup.mainloop()

    def select_all(self):
        """
        Selects all options (checkboxes)
        """
        logging.debug("Selecting all choices")
        for option in self.options_choices.chks:
            option.select()

    def deselect_all(self):
        """
        Deselects all options (checkboxes)
        """
        logging.debug("Deselecting all choices")
        for option in self.options_choices.chks:
            option.deselect()

    def close_window(self):
        """
        Closes the window, destroys it and exits the program
        """
        logging.info("Closing window")
        self.window.destroy()
        sys.exit()

    def close_window_escape(self, event):
        """
        Closes the window, destroys it and exits the program

        :param event: Key press event
        """
        logging.info("Closing window")
        self.window.destroy()
        sys.exit()

    def get_project_path(self):
        """
        Callback used when use sets the directory.
        """
        # @todo: Add default path (Based on OS)
        logging.debug("Asking for path")
        self.path = filedialog.askdirectory()
        logging.info("User gave path `{}`".format(self.path))

    def start(self):
        if not self.project_name:
            logging.error("Project not specified")
            messagebox.showerror("Project not specified", "You need to specify the project you want to test.")
            return
        if not self.path:
            logging.error("Path not specified")
            messagebox.showerror("Path not specified", "You need to specify the path of the project you want to test.")
            return
        if not self.project_name == "42commandements":
            has_selected = 0
            for choice in self.options_choices.state():
                if choice == 1:
                    has_selected = 1
                    break
            if not has_selected:
                logging.warning("No options passed")
                messagebox.showwarning("No options", "You havent selected any options.")
                return
        print(self.project_name)
        print(self.path)
        print(list(self.options_choices.state()))
        self.set_args()
        self.start_project()

    def start_project(self):
        if self.project_name == "other":
            logging.info("Starting {} project check".format(self.project_name))
            other.check(self.root_path, self.args)

    def set_args(self):
        self.reset_args()
        choices = list(self.options_choices.state())
        if self.project_name == "other":
            logging.debug("Setting args for project {}".format(self.project_name))
            self.args.path = self.path
            if choices[0]:
                self.args.no_author = False
            if not choices[1]:
                self.args.no_norme = False
            if not choices[2]:
                self.args.no_makefile = False

    def reset_args(self):
        logging.debug("Resetting args")
        self.args.no_libftest = True
        self.args.no_maintest = True
        self.args.no_moulitest = True
        self.args.no_author = True
        self.args.no_forbidden = True
        self.args.no_makefile = True
        self.args.no_norm = True
        self.args.no_static = True
        self.args.no_extra = True
        self.args.no_tests = True
        self.args.no_required = True
        self.args.no_libft_unit_test = True
        self.args.do_benchmark = True
        self.args.no_fillit = True
        self.args.no_bonus = True

    def update_options(self, *args):
        """
        Updates the checkboxes option list.
        :param args: No idea what that is
        """
        logging.debug("Updating checkboxes options")
        self.project_name = self.project.get()
        self.options = self.options_dict[self.project.get()]
        self.options_choices.destroy()
        self.options_choices = Checkbar(self.window, self.options)
        self.options_choices.pack(side=BOTTOM)
