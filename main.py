#!/usr/bin/env python3
import os
import platform
from tkinter import *
from tkinter import messagebox
from file_manager.view import FileManagerView
from file_manager.model import FileManagerModel
from file_manager.presenter import FileManagerPresenter


if platform.system() != "Linux":
    messagebox.showerror("Error", "unsupported system")
else:

    root = Tk()
    gui = FileManagerView(root)

    brain = FileManagerModel()

    fm = FileManagerPresenter(gui, brain)

    brain.item_selection(gui.tree_right, os.path.expanduser("~"))
    brain.item_selection(gui.tree_left, os.path.expanduser("~"))

    fm.current_dir_path(gui, gui.tree_right, os.path.expanduser("~"))
    fm.current_dir_path(gui, gui.tree_left, os.path.expanduser("~"))

    root.mainloop()
