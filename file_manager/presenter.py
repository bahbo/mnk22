from tkinter import *
import os
from pathlib import Path


class FileManagerPresenter:
    def __init__(self, view, model):
        self.last_selection_tree_1 = None
        self.last_selection_tree_2 = None
        self.tree_paths = {view.tree_left: None, view.tree_right: None}
        self.tv_order = [view.tree_left, view.tree_right]

        view.root.bind("<Configure>", lambda event: view.move_user_window())

        view.tree_left.bind(
            "<Double-Button-1>",
            lambda event: self.item_selected_click(model, view, view.tree_left, event),
        )
        view.tree_right.bind(
            "<Double-Button-1>",
            lambda event: self.item_selected_click(model, view, view.tree_right, event),
        )

        view.tree_left.bind(
            "<Return>",
            lambda event: self.item_selected_enter(model, view, view.tree_left),
        )
        view.tree_right.bind(
            "<Return>",
            lambda event: self.item_selected_enter(model, view, view.tree_right),
        )

        view.tree_left.bind(
            "<FocusIn>", lambda event: self.toggle_tv(view.tree_left, view)
        )
        view.tree_right.bind(
            "<FocusIn>", lambda event: self.toggle_tv(view.tree_right, view)
        )

        view.tree_left.bind(
            "<<TreeviewSelect>>", lambda event: self.active_selection(view)
        )
        view.tree_right.bind(
            "<<TreeviewSelect>>", lambda event: self.active_selection(view)
        )

        view.f1.configure(command=lambda: self.info(model, view))
        view.root.bind("<F1>", lambda event: self.info(model, view))

        view.f2.configure(command=lambda: self.rename(model, view))
        view.root.bind("<F2>", lambda event: self.rename(model, view))

        view.f3.configure(command=lambda: self.cut_refresh(view, model))
        view.root.bind("<F3>", lambda event: self.cut_refresh(view, model))
        view.root.bind("<Control-x>", lambda event: self.cut_refresh(view, model))

        view.f4.configure(command=lambda: self.copy_refresh(view, model))
        view.root.bind("<F4>", lambda event: self.copy_refresh(view, model))
        view.root.bind("<Control-c>", lambda event: self.copy_refresh(view, model))

        view.f5.configure(
            command=lambda: model.paste(self.tv_list(view), self.tree_paths, view)
        )
        view.root.bind(
            "<F5>", lambda event: model.paste(self.tv_list(view), self.tree_paths, view)
        )
        view.root.bind(
            "<Control-v>",
            lambda event: model.paste(self.tv_list(view), self.tree_paths, view),
        )

        view.f6.configure(command=lambda: self.change_permissions(model, view))
        view.root.bind("<F6>", lambda event: self.change_permissions(model, view))

        view.f7.configure(command=lambda: self.change_owner_group(model, view))
        view.root.bind("<F7>", lambda event: self.change_owner_group(model, view))

        view.f8.configure(command=lambda: self.search(model, view))
        view.root.bind("<F8>", lambda event: self.search(model, view))

        view.f9.configure(command=lambda: self.toggle_tree_info(view))
        view.root.bind("<F9>", lambda event: self.toggle_tree_info(view))

        view.f10.configure(
            command=lambda: model.delete_file_dir(self.active_selection(view), view)
        )
        view.root.bind(
            "<F10>",
            lambda event: model.delete_file_dir(self.active_selection(view), view),
        )

        view.f11.configure(command=lambda: view.root.destroy())
        view.root.bind("<F11>", lambda event: view.root.destroy())

    def tv_list(self, view):
        """
        List of display panels. Sorts the list so the active panel is at first position.

        Args:
            view: class FileManagerView
        """

        if len(view.tree_left.selection()) > 0:
            self.tv_order = [view.tree_left, view.tree_right]
        elif len(view.tree_right.selection()) > 0:
            self.tv_order = [view.tree_right, view.tree_left]
        return self.tv_order

    #
    def active_selection(self, view):
        """
        Displays current selection in each panel.

        Args:
            view: class FileManagerView
        """

        if len(view.tree_left.selection()) > 0:
            view.active_pos_left.set(
                view.tree_left.item(view.tree_left.selection())["values"][0]
            )
            return view.tree_left.item(view.tree_left.focus())
        elif len(view.tree_right.selection()) > 0:
            view.active_pos_right.set(
                view.tree_right.item(view.tree_right.selection())["values"][0]
            )
            return view.tree_right.item(view.tree_right.focus())

    #
    def info(self, model, view):
        """
        Show system information.

        Args:
            model: class FileManagerModel
            view: class FileManagerView
        """
        view.info_screen()

        for index, value in enumerate(model.system_information()):
            view.info_frame.grid_slaves(row=index, column=0)[0].configure(text=value[0])
            view.info_frame.grid_slaves(row=index, column=1)[0].configure(text=value[1])
        view.ok_button.grid(row=2, column=0, columnspan=2, pady=(0, 10))
        view.uw_label.configure(text="System Information")
        view.u_window_position()

    #
    def rename(self, model, view):
        """
        Rename selected object.

        Args:
            model: class FileManagerModel
            view: class FileManagerView
        """
        path = self.active_selection(view)["text"]
        if self.active_selection(view)["values"][0] != "/..":
            view.rename()
            view.uw_label.configure(text="Enter New Name:")
            view.entry_text.set(Path(path).name)
            view.ok_button.configure(command=lambda: model.rename(path, view))

    def cut_refresh(self, view, model):
        """
        Updates UI to show cut objects.

        Args:
            model: class FileManagerModel
            view: class FileManagerView
        """
        model.cut_file_folder(self.active_selection(view), view)
        self.toggle_tv(self.tv_list(view)[0], view)
        self.toggle_tv(self.tv_list(view)[0], view)

    def copy_refresh(self, view, model):
        """
        Updates UI to show copied objects.

        Args:
            model: class FileManagerModel
            view: class FileManagerView
        """
        model.copy_file_folder(self.active_selection(view), view)
        self.toggle_tv(self.tv_list(view)[0], view)
        self.toggle_tv(self.tv_list(view)[0], view)

    def change_permissions(self, model, view):
        """
        Change objects permissions.

        Args:
            model: class FileManagerModel
            view: class FileManagerView
        """
        path = self.active_selection(view)["text"]
        if self.active_selection(view)["values"][0] != "/..":
            view.chmod_window()
            view.uw_label.configure(text=f"chmod: {Path(path).name}")
            view.uf_perm.grid(row=1, column=0, columnspan=2, pady=10, padx=20)
            view.uw_label.configure(text=f"chmod: {Path(path).name}")
            model.get_obj_perm(path, view.permissions)
            view.ok_button.configure(
                command=lambda: model.set_obj_perm(path, view.permissions, view)
            )

    #
    def change_owner_group(self, model, view):
        """
        Change objects group or/and owner.

        Args:
            model: class FileManagerModel
            view: class FileManagerView
        """
        path = self.active_selection(view)["text"]
        if self.active_selection(view)["values"][0] != "/..":
            view.chown_window()
            view.uw_label.configure(text=f"chown: {Path(path).name}")
            view.cb_groups.configure(values=model.get_groups())
            view.groups_var.set(Path(path).group())
            view.cb_users.configure(values=model.get_users())
            view.users_var.set(Path(path).owner())
            view.ok_button.configure(command=lambda: model.obj_chown(path, view))

    #
    def search(self, model, view):
        """
        Search for file or folder.

        Args:
            model: class FileManagerModel
            view: class FileManagerView
        """
        view.search_window()
        view.uw_label.configure(text="Search in:")

        view.cb_search_dir.configure(values=["current dir", "home", "all"])
        view.cb_search_dir_var.set("current dir")
        if view.cb_search_dir_var.get() == "current dir":
            path = self.tree_paths[self.tv_list(view)[0]]
        elif view.cb_search_dir_var.get() == "home":
            path = os.path.expanduser("~")
        else:
            path = "/"
        view.ok_button.configure(
            command=lambda: model.search_alg(
                path,
                self.tv_list(view),
                view.entry_text.get(),
                view.destroy_user_window,
            )
        )

    #
    def toggle_tree_info(self, view):
        """
        Changes active panel listing mode. /Standard, Full/

        Args:
            view: class FileManagerView
        """
        tv = self.tv_list(view)[0]
        if tv["displaycolumns"] == ("#1", "#2", "#3"):
            tv["displaycolumns"] = ("#1", "#2", "#3", "#4", "#5", "#6")
            tv.heading("#4", text="Permissions")
            tv.heading("#5", text="Owner")
            tv.heading("#6", text="Group")

            tv.column("#1", minwidth=250, width=250)
            tv.column("#2", width=75, stretch=False, anchor=E)
            tv.column("#3", width=120, stretch=False)
            tv.column("#4", width=120, stretch=False)
            tv.column("#5", width=60, stretch=False, anchor=CENTER)
            tv.column("#6", width=60, stretch=False, anchor=CENTER)
            tv.event_generate("<<ThemeChanged>>")
        else:
            tv["displaycolumns"] = ("#1", "#2", "#3")
            tv.column("#1", minwidth=250, width=250)
            tv.column("#2", width=75, stretch=False, anchor=E)
            tv.column("#3", width=120, stretch=False)
            tv.event_generate("<<ThemeChanged>>")

    #
    def current_dir_path(self, view, tv, path):
        """
        Displays current directory of each panel.

        Args:
            view: view: class FileManagerView
            tv: active panel
            path: current directory path
        """
        if Path(path).is_dir():
            if tv == view.tree_left:
                self.tree_paths[view.tree_left] = path
                view.lf_topleft_var.set(path)
            else:
                self.tree_paths[view.tree_right] = path
                view.lf_topright_var.set(path)

    #
    def item_selected_click(self, model, view, tree_view, event):
        """
        Selecting directory or opening a document with mouse click.

        Args:
            model: class FileManagerModel
            view: class FileManagerView
            tree_view: active panel
            event: mouse click
        """
        region = tree_view.identify("region", event.x, event.y)
        if region == "heading":
            pass
        elif region == "cell":
            self.item_selected_enter(model, view, tree_view)

    #
    def item_selected_enter(self, model, view, tree_view):
        """
        Selecting directory or opening a document.

        Args:
            model: class FileManagerModel
            view: class FileManagerView
            tree_view: active panel
        """
        selected_path = tree_view.item(tree_view.selection())["text"]
        model.item_selection(tree_view, selected_path)
        self.current_dir_path(view, tree_view, selected_path)

    #
    def toggle_tv(self, tv, view):
        """Switch between panels: tree_left, tree_right."""
        if tv == view.tree_left:
            self.last_selection_tree_1 = view.tree_left.focus()
            view.tree_left.selection_set(self.last_selection_tree_1)
            view.tree_right.selection_toggle(view.tree_right.selection())
            view.lf_topright_label.configure(style="TLabelframe.Label")
            view.lf_topleft_label.configure(style="New.TLabelframe.Label")
        else:
            self.last_selection_tree_2 = view.tree_right.focus()
            view.tree_right.selection_set(self.last_selection_tree_2)
            view.tree_left.selection_toggle(view.tree_left.selection())
            view.lf_topleft_label.configure(style="TLabelframe.Label")
            view.lf_topright_label.configure(style="New.TLabelframe.Label")
