from tkinter import *
from tkinter import messagebox
import os
import stat
from pathlib import Path
import shutil
from datetime import datetime
import pwd
import platform
import cpuinfo
import psutil
import subprocess


class FileManagerModel:
    def __init__(self):
        self.sys_info = None
        self.tree_paths = []
        self.copied_object = None
        self.cut_object = None
        self.permission_keys = [
            stat.S_IRUSR,
            stat.S_IWUSR,
            stat.S_IXUSR,
            stat.S_IRGRP,
            stat.S_IWGRP,
            stat.S_IXGRP,
            stat.S_IROTH,
            stat.S_IWOTH,
            stat.S_IXOTH,
        ]

    def get_size(self, bytes_, suffix="B"):
        """Scale bytes to its proper format"""
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes_ < factor:
                return f"{bytes_:.0f}{unit}{suffix}"
            bytes_ /= factor

    def open_dir(self, path):
        """
        Makes a list of entries in certain directory.

        Args:
            path: directory path
        """

        self.tree_paths = {"dirs": [], "files": [], "broken links": []}
        if path != os.path.abspath(os.sep):
            up_dir = (Path(path).parent, "/..", "UP--DIR")
            self.tree_paths["dirs"].append(up_dir)

        for item in os.scandir(path):

            # add broken links
            if Path(item).is_symlink() and not os.path.exists(os.readlink(item)):
                info = [item.path, item.name]
                self.tree_paths["broken links"].append(info)
            else:
                info = [
                    item.path,
                    item.name,
                    self.get_size(item.stat().st_size),
                    datetime.fromtimestamp(item.stat().st_mtime).strftime("%b %d %-H:%M"),
                    stat.filemode(item.stat().st_mode),
                    Path(item.path).owner(),
                    Path(item.path).group(),
                ]
                # add dirs
                if item.is_dir():
                    info[1] = f"/{item.name}"
                    self.tree_paths["dirs"].append(info)
                # add files
                else:
                    self.tree_paths["files"].append(info)

        for key, value in self.tree_paths.items():
            value.sort(key=lambda x: x[1])
        return self.tree_paths

    #
    def item_selection(self, tv, path):
        """
        Depending on path (file or folder): open document or displays directory content.

        Args:
            tv: active panel
            path: file or dir path
        """
        if os.path.isfile(path):
            subprocess.call(["xdg-open", path])
        elif Path(path).is_symlink() and not os.path.exists(os.readlink(path)):
            messagebox.showerror("Error", f"path {Path(path).name} is a broken symlink")

        else:
            try:
                dir_items = self.open_dir(path)
            except PermissionError as pe:
                messagebox.showerror("Error", pe.strerror)

            else:
                for entry in tv.get_children():
                    tv.delete(entry)

                for key, values in dir_items.items():
                    if key == "dirs":
                        for item in values:
                            if item[0] == self.copied_object or item[0] == self.cut_object:
                                tv.insert("", END, tags="cut_copy", text=item[0], values=tuple(item[1:]))
                            else:
                                tv.insert("", END, tags="dir", text=item[0], values=tuple(item[1:]))
                    else:
                        for item in values:
                            if item[0] == self.copied_object or item[0] == self.cut_object:
                                tv.insert("", END, tags="cut_copy", text=item[0], values=tuple(item[1:]))
                            else:
                                tv.insert("", END, tags="file", text=item[0], values=tuple(item[1:]))

                tv.focus(tv.get_children()[0])
                tv.selection_set(tv.get_children()[0])

    def close_user_window(self, view):
        """
        Closes the dialog screen and updates information panels.

        Args:
            view: class FileManagerView
        """
        view.destroy_user_window()
        self.update_tv(view)

    def update_tv(self, view):
        """
        Updates information panels.

        Args:
            view: class FileManagerView
        """
        self.item_selection(view.tree_left, view.lf_topleft_var.get())
        self.item_selection(view.tree_right, view.lf_topright_var.get())

    #
    def rename(self, path, view):
        """
        Rename a file or directory.

        Args:
            path: object path
            view: class FileManagerView
        """
        entry_text = view.entry_text
        base_path = str(Path(path).parent)
        new_name = os.path.join(base_path, entry_text.get())
        if os.path.exists(new_name):
            messagebox.showerror("Error", f"Already exists", parent=view.u_window)

        else:
            try:
                os.rename(path, new_name)
            except PermissionError as pe:
                messagebox.showerror("Error", pe.strerror, parent=view.u_window)

        if path in view.lf_topleft_var.get():
            view.lf_topleft_var.set(view.lf_topleft_var.get().replace(path, new_name))
        if path in view.lf_topright_var.get():
            view.lf_topright_var.set(view.lf_topright_var.get().replace(path, new_name))
        self.close_user_window(view)

    #
    def delete_file_dir(self, selection, view):
        """
        Delete a file or directory.

        Args:
            selection: object path
            view: class FileManagerView
        """
        path = selection["text"]
        if selection["values"][0] != "/..":
            if messagebox.askyesno(
                "Delete", f"Are you sure you want to delete {selection['values'][0]}?"
            ):
                try:
                    if os.path.isfile(path) or os.path.islink(path):
                        os.remove(path)
                    elif os.path.isdir(path):
                        shutil.rmtree(path)
                except PermissionError as pe:
                    messagebox.showerror("Error", pe.strerror)

                if path in view.lf_topleft_var.get():
                    view.lf_topleft_var.set(str(Path(path).parent))
                if path in view.lf_topright_var.get():
                    view.lf_topright_var.set(str(Path(path).parent))
                self.update_tv(view)

    #
    def copy_file_folder(self, selection, view):
        """
        Marks file or directory ready to be copied.

        Args:
            selection: object path
            view: class FileManagerView
        """
        path = selection["text"]
        if selection["values"][0] != "/..":
            self.copied_object = path
            self.cut_object = None
            self.update_tv(view)

    def cut_file_folder(self, selection, view):
        """
        Marks file or directory ready to be moved.

        Args:
            selection: object path
            view: class FileManagerView
        """
        path = selection["text"]
        if selection["values"][0] != "/..":
            self.copied_object = None
            self.cut_object = path
            self.update_tv(view)

    def paste_copied_object(self, location):
        """
        Makes copy of file or directory in selected location.

        Args:
            location: destination path
        """
        name = Path(self.copied_object).name
        new_path = os.path.join(location, name)
        if Path.exists(Path(new_path)):
            question = messagebox.askquestion(
                "Error", "Path already exists./nDo you want to replace it?"
            )
            if question == "yes":
                if os.path.isfile(self.copied_object) or os.path.islink(
                    self.copied_object
                ):
                    shutil.copy2(self.copied_object, new_path)
                elif os.path.isdir(self.copied_object):
                    shutil.copytree(self.copied_object, new_path)
        else:
            if os.path.isfile(self.copied_object) or os.path.islink(self.copied_object):
                shutil.copy2(self.copied_object, new_path)
            elif os.path.isdir(self.copied_object):
                shutil.copytree(self.copied_object, new_path)

    #
    def paste_cut_object(self, location):
        """
        Moves file or directory in selected location.

        Args:
            location: destination path
        """
        name = Path(self.cut_object).name
        new_path = os.path.join(location, name)
        if Path.exists(Path(new_path)):
            question = messagebox.askquestion(
                "Error", "Path already exists./nDo you want to replace it?"
            )
            if question == "yes":
                shutil.move(self.cut_object, new_path)
        else:
            shutil.move(self.cut_object, new_path)

    #
    def paste(self, tv_list, tree_paths, view):
        """
         Moves/makes copy of file or directory in selected location.

        Args:
            tv_list: active panel
            tree_paths: current directory in the active panel
            view: class FileManagerView
        """
        location = tree_paths[tv_list[0]]
        try:
            if self.copied_object is not None:
                self.paste_copied_object(location)
            elif self.cut_object is not None:
                self.paste_cut_object(location)

        except PermissionError as pe:
            messagebox.showerror("Error", pe.strerror)

        if str(self.cut_object) in view.lf_topleft_var.get():
            view.lf_topleft_var.set(
                view.lf_topleft_var.get().replace(str(self.cut_object), str(location))
            )
        elif str(self.cut_object) in view.lf_topright_var.get():
            view.lf_topright_var.set(
                view.lf_topright_var.get().replace(str(self.cut_object), str(location))
            )
        self.copied_object = None
        self.cut_object = None
        self.update_tv(view)

    def get_obj_perm(self, path, perm):
        """
        Get current permissions for file or folder.

        Args:
            path: file or directory path.
            perm: list of permissions
        """
        for x in range(len(perm)):
            if bool(os.stat(path).st_mode & self.permission_keys[x]):
                perm[x][1].set(1)

    #
    def set_obj_perm(self, path, perm, view):
        """
        Set permissions for file or folder.

        Args:
            path: file or directory path.
            perm: list of permissions
            view: class FileManagerView
        """
        new_perm = 0
        for x in range(len(perm)):
            if perm[x][1].get() == 1:
                new_perm += self.permission_keys[x]
        try:
            os.chmod(path, new_perm)
            self.close_user_window(view)
        except PermissionError as pe:
            self.close_user_window(view)
            messagebox.showerror("Error", pe.strerror)

    #
    def get_groups(self):
        """
        Get a list of user groups.
        """
        data = []
        with open("/etc/group", "r") as f:
            for line in f.readlines():
                data.append(line.split(":")[0])
        data.sort()
        return data

    def get_users(self):
        """
        Get a list of users.
        """
        data = []
        for p in pwd.getpwall():
            if p[0] not in data:
                data.append(p[0])
        data.sort()
        return data

    def obj_chown(self, path, view):
        """
        Changes ownership of file or directory.

        Args:
            path: file or directory path.
            view: class FileManagerView
        """
        users = view.users_var
        groups = view.groups_var
        c_user = Path(path).owner()
        c_group = Path(path).group()
        try:
            if c_user == users and c_group != groups:
                shutil.chown(path, group=groups.get())
            elif c_user != users and c_group == groups:
                shutil.chown(path, user=users.get())
            elif c_user != users and c_group != groups:
                shutil.chown(path, user=users.get(), group=groups.get())
            self.close_user_window(view)
        except PermissionError as pe:
            self.close_user_window(view)
            messagebox.showerror("Error", pe.strerror)

    #
    def rec_split(self, path):
        """
        Shorten file or directory path.

        Args:
            path: file or directory path
        """
        short_path = path.split("/", 1)[1]
        while len(short_path) > 60:
            path = path.split("/", 1)[1]
            short_path = path
        return f"/{short_path}"

    def search_alg(self, search_dir, tv_list, name, destroy_user_window):
        """
        Makes a list of search entries in certain directory.

        Args:
            search_dir: directory to search in
            tv_list: panel to display results
            name: search entry
            destroy_user_window: close dialog screen
        """

        tv = tv_list[0]

        for entry in tv.get_children():
            tv.delete(entry)

        tv.insert("", END, tags="dir", text=search_dir, values=("/..", "UP--DIR"))
        results = []
        for root, dirs, files in os.walk(search_dir):
            for file in files:
                if name.lower() in file.lower():
                    results.append(root + "/" + str(file))
            for dir_ in dirs:
                if name.lower() in dir_.lower():
                    results.append(root + "/" + str(dir_))

        results = [
            [
                item,
                self.rec_split(item),
                self.get_size(Path(item).stat().st_size),
                datetime.fromtimestamp(Path(item).stat().st_mtime).strftime("%b %d %-H:%M"),
                stat.filemode(Path(item).stat().st_mode),
                Path(item).owner(),
                Path(item).group(),
            ]
            for item in results
        ]

        for item in results[1:]:
            if Path(item[0]).is_dir():
                tv.insert("", END, tags="dir", text=item[0], values=tuple(item[1:]))
        for item in results[1:]:
            if Path(item[0]).is_file():
                tv.insert("", END, tags="file", text=item[0], values=tuple(item[1:]))

        destroy_user_window()

    def system_information(self):
        """Get system information."""
        total, used, free = shutil.disk_usage("/")
        uname = platform.uname()
        self.sys_info = [
            ["System: ", uname.system],
            ["Current User: ", pwd.getpwuid(os.getuid())[0]],
            ["Node Name: ", uname.node],
            ["Release: ", uname.release],
            ["Version: ", uname.version],
            ["Machine: ", uname.machine],
            ["Processor: ", cpuinfo.get_cpu_info()["brand_raw"]],
            ["Physical cores: ", psutil.cpu_count(logical=False)],
            ["Total cores: ", psutil.cpu_count(logical=True)],
            ["Total memory: ", self.get_size(psutil.virtual_memory().total)],
            ["Total disk space: ", self.get_size(total)],
            ["Used disk space: ", self.get_size(used)],
            ["Free disk space: ", self.get_size(free)],
        ]
        return self.sys_info
