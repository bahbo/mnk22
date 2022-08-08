from tkinter import *
from tkinter import ttk


class MainWindow:
    """
    Provides the main interface. Defines the style and theme of the application.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("File Manager")

        self.my_style = ttk.Style()
        self.my_style.configure("Label", font=("Monospace", 11))

        self.my_style.configure(
            "New.TLabel",
            background="#00458b",
            foreground="light gray",
            font=("Monospace", 11),
        )

        self.my_style.configure(
            "Treeview.Heading",
            font=("Monospace", 11),
            background="#00458b",
            foreground="yellow",
        )
        self.my_style.map(
            "Treeview.Heading",
            foreground=[("pressed", "yellow"), ("active", "yellow")],
            background=[("pressed", "#00458b"), ("active", "#00458b")],
        )

        self.my_style.configure(
            "Treeview",
            fieldbackground="#00458b",
            borderwidth=0,
            background="#00458b",
            font=("Monospace", 11),
        )
        self.my_style.map(
            "Treeview",
            background=[("selected", "cyan4")],
            foreground=[("selected", "black")],
        )

        self.my_style.map(
            "TButton",
            relief=FLAT,
            background=[
                ("pressed", "cyan4"),
                ("active", "cyan4"),
                ("!active", "cyan4"),
            ],
        )

        self.my_style.configure(
            "TLabelframe.Label",
            foreground="light gray",
            background="#00458b",
            font=("Monospace", 11),
        )

        self.my_style.configure("TLabelframe", background="#00458b")

        self.my_style.configure(
            "New.TLabelframe.Label",
            foreground="black",
            background="cyan4",
            font=("Monospace", 11),
        )

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

        self.tree_frame_left = ttk.Frame(
            self.root,
        )
        self.tree_frame_left.grid(row=0, column=0, sticky=NSEW)

        self.tree_frame_right = ttk.Frame(self.root)
        self.tree_frame_right.grid(row=0, column=1, sticky=NSEW)

        self.lf_topleft_var = StringVar()
        self.lf_topleft_label = ttk.Label(
            self.tree_frame_left, textvariable=self.lf_topleft_var
        )
        self.lf_topleft = ttk.LabelFrame(
            self.tree_frame_left, labelwidget=self.lf_topleft_label
        )
        self.lf_topleft.pack(
            fill="both",
            side=TOP,
            expand=True,
        )

        self.lf_topright_var = StringVar()
        self.lf_topright_label = ttk.Label(
            self.tree_frame_right, textvariable=self.lf_topright_var
        )
        self.lf_topright = ttk.LabelFrame(
            self.tree_frame_right, labelwidget=self.lf_topright_label
        )
        self.lf_topright.pack(fill="both", side=TOP, expand=True)

        self.bottomleft_lf = ttk.LabelFrame(
            self.tree_frame_left, text="Current Selections", labelanchor=SE
        )
        self.bottomleft_lf.pack(fill=X, side=TOP, expand=False)

        self.bottomright_lf = ttk.LabelFrame(
            self.tree_frame_right, text="Current Selections", labelanchor=SE
        )
        self.bottomright_lf.pack(fill=X, side=TOP, expand=False)

        self.active_pos_left = StringVar()
        self.but = ttk.Label(
            self.bottomleft_lf, textvariable=self.active_pos_left, style="New.TLabel"
        )
        self.but.pack(side=LEFT)

        self.active_pos_right = StringVar()
        self.but2 = ttk.Label(
            self.bottomright_lf, textvariable=self.active_pos_right, style="New.TLabel"
        )
        self.but2.pack(side=LEFT)

        self.tree_left = ttk.Treeview(
            self.lf_topleft,
            columns=("#1", "#2", "#3", "#4", "#5", "#6"),
            show="headings",
            selectmode="browse",
        )
        self.tree_left.pack(fill="both", side=LEFT, expand=True)

        self.tree_left.focus_set()

        self.tree_right = ttk.Treeview(
            self.lf_topright,
            columns=("#1", "#2", "#3", "#4", "#5", "#6"),
            show="headings",
            selectmode="browse",
        )
        self.tree_right.pack(fill="both", side=LEFT, expand=True)

        #
        for tree in (self.tree_left, self.tree_right):
            tree["displaycolumns"] = ("#1", "#2", "#3")
            tree.tag_configure("dir", foreground="light gray")
            tree.tag_configure("file", foreground="cyan4")
            tree.tag_configure("cut_copy", foreground="yellow")

            tree.heading(
                "#1",
                text="Name",
            )
            tree.heading("#2", text="Size")
            tree.heading("#3", text="Modify time")

            tree.column("#1", minwidth=250, width=250)
            tree.column("#2", width=75, stretch=False, anchor=E)
            tree.column("#3", width=120, stretch=False)

        self.b_frame = Frame(self.root)
        self.b_frame.grid(row=4, column=0, columnspan=2, sticky=EW)

        self.f1 = ttk.Button(self.b_frame, text="F1 Info", takefocus=0, underline=1)
        self.f1.grid(row=0, column=0, sticky=EW)

        self.f2 = ttk.Button(self.b_frame, text="F2 Rename", takefocus=0, underline=1)
        self.f2.grid(row=0, column=1, sticky=EW)

        self.f3 = ttk.Button(self.b_frame, text="F3 Cut", takefocus=0, underline=1)
        self.f3.grid(row=0, column=2, sticky=EW)

        self.f4 = ttk.Button(self.b_frame, text="F4 Copy", takefocus=0, underline=1)
        self.f4.grid(row=0, column=3, sticky=EW)

        self.f5 = ttk.Button(self.b_frame, text="F5 Paste", takefocus=0, underline=1)
        self.f5.grid(row=0, column=4, sticky=EW)

        self.f6 = ttk.Button(self.b_frame, text="F6 Chmod", takefocus=0, underline=1)
        self.f6.grid(row=0, column=5, sticky=EW)

        self.f7 = ttk.Button(self.b_frame, text="F7 Chown", takefocus=0, underline=1)
        self.f7.grid(row=0, column=6, sticky=EW)

        self.f8 = ttk.Button(self.b_frame, text="F8 Search", takefocus=0, underline=1)
        self.f8.grid(row=0, column=7, sticky=EW)

        self.f9 = ttk.Button(self.b_frame, text="F09 Panel", takefocus=0, underline=1)
        self.f9.grid(row=0, column=8, sticky=EW)

        self.f10 = ttk.Button(self.b_frame, text="F10 Delete", takefocus=0, underline=1)
        self.f10.grid(row=0, column=9, sticky=EW)

        self.f11 = ttk.Button(self.b_frame, text="F11 Quit", takefocus=0, underline=1)
        self.f11.grid(row=0, column=10, sticky=EW)

        for x in range(10):
            self.b_frame.columnconfigure(x, weight=1, uniform="label")


class FileManagerView(MainWindow):
    """
    Adds different dialog screens to the UI.
    """

    def __init__(self, root):
        super().__init__(root)
        self.permissions = None
        self.cb_search_dir = None
        self.cb_search_dir_var = None
        self.cb_groups = None
        self.groups_var = None
        self.lf_group = None
        self.cb_users = None
        self.users_var = None
        self.lf_owner = None
        self.uf_owner = None
        self.uf_perm = None
        self.info_frame = None
        self.cancel_button = None
        self.ok_button = None
        self.uw_entry = None
        self.entry_text = None
        self.u_window = None
        self.uw_label = None

    def accepted_characters(self, char):
        """
        Validates char != '/'.
        Used as validatecommand in Entry widget.

        Args:
            char: str
        """
        if char != "/":
            return True
        return False

    def u_window_position(self):
        """Places the dialog screen in the center of main window."""
        self.u_window.update()
        x_r = self.root.winfo_x()
        y_r = self.root.winfo_y()
        w_r = self.root.winfo_width()
        h_r = self.root.winfo_height()

        w_uf = self.u_window.winfo_width()
        h_uf = self.u_window.winfo_height()
        self.u_window.geometry(f"+{x_r + (w_r - w_uf) // 2}+{y_r + (h_r - h_uf) // 2}")

    def move_user_window(self):
        """Moves dialog screen with main window."""
        if self.u_window is not None:
            self.u_window_position()

    def destroy_user_window(self):
        """Closes the dialog screen."""
        self.u_window.destroy()
        self.u_window = None

    def show_user_window(self):
        """Displays the dialog screen."""
        self.u_window = Toplevel(self.root)
        self.u_window.transient(self.root)
        self.u_window.wm_attributes("-type", "splash")
        self.u_window.grab_set()

    def add_label(self):
        """Adds label widget to the dialog screen."""
        self.uw_label = ttk.Label(self.u_window)
        self.uw_label.grid(row=0, column=0, columnspan=2, pady=(10, 0))

    def add_buttons(self):
        """Adds <OK> and <Cancel> buttons to the dialog screen."""
        self.ok_button = ttk.Button(self.u_window, text="OK")
        self.ok_button.grid(row=2, column=0, pady=(0, 10))

        self.cancel_button = ttk.Button(
            self.u_window, text="Cancel", command=self.destroy_user_window
        )
        self.cancel_button.grid(row=2, column=1, pady=(0, 10))

    def add_entry(self):
        """Adds entry widget to the dialog screen."""
        vcmd = (self.root.register(self.accepted_characters), "%S")
        self.entry_text = StringVar()
        self.uw_entry = Entry(
            self.u_window,
            width=25,
            textvariable=self.entry_text,
            validate="key",
            vcmd=vcmd,
        )
        self.uw_entry.grid(
            row=1, column=0, columnspan=2, ipady=3, pady=10, padx=20, sticky=NSEW
        )

    def info_screen(self):
        """Displays dialog screen with system information."""
        self.show_user_window()
        self.add_label()
        self.ok_button = ttk.Button(
            self.u_window, text="OK", command=self.destroy_user_window
        )

        self.info_frame = Frame(self.u_window)
        self.info_frame.grid(row=1, column=0, columnspan=2, pady=10, padx=20)
        for i in range(13):
            Label(self.info_frame, anchor=W).grid(row=i, column=0, sticky=EW)
            Label(self.info_frame, anchor=W).grid(row=i, column=1, sticky=EW)
        self.u_window_position()

    #
    def rename(self):
        """Displays dialog screen for renaming file or directory."""
        self.show_user_window()
        self.add_label()
        self.add_entry()
        self.add_buttons()
        self.u_window_position()

    def chmod_window(self):
        """Displays dialog screen for changing file or directory permissions."""
        var_irusr = IntVar()
        var_iwusr = IntVar()
        var_ixusr = IntVar()
        var_irgrp = IntVar()
        var_iwgrp = IntVar()
        var_ixgrp = IntVar()
        var_iroth = IntVar()
        var_iwoth = IntVar()
        var_ixoth = IntVar()

        self.permissions = [
            ["Read by owner", var_irusr],
            ["Write by owner", var_iwusr],
            ["Execute by owner", var_ixusr],
            ["Read by group", var_irgrp],
            ["Write by group", var_iwgrp],
            ["Execute by group", var_ixgrp],
            ["Read by others", var_iroth],
            ["Write by others", var_iwoth],
            ["Execute by others", var_ixoth],
        ]

        self.show_user_window()
        self.add_label()
        self.add_buttons()
        self.uf_perm = ttk.Frame(self.u_window)
        self.uf_perm.grid(row=1, column=0, columnspan=2, pady=10, padx=20)
        for index, value in enumerate(self.permissions):
            Checkbutton(self.uf_perm, text=value[0], variable=value[1]).grid(
                row=index, column=1, sticky=W
            )
        self.u_window_position()

    #
    def chown_window(self):
        """Displays dialog screen for changing file or directory ownership."""
        self.show_user_window()
        self.add_label()
        self.add_buttons()
        self.uf_owner = ttk.Frame(self.u_window)
        self.uf_owner.grid(row=1, column=0, columnspan=2, pady=10, padx=20)

        self.lf_owner = LabelFrame(self.uf_owner, text="User", labelanchor=N)
        self.lf_owner.grid(column=0, row=0)
        self.users_var = StringVar()
        self.cb_users = ttk.Combobox(
            self.lf_owner,
            textvariable=self.users_var,
            justify="center",
            state="readonly",
        )
        self.cb_users.grid(column=0, row=0)

        self.lf_group = LabelFrame(self.uf_owner, text="Group", labelanchor=N)
        self.lf_group.grid(column=1, row=0)
        self.groups_var = StringVar()
        self.cb_groups = ttk.Combobox(
            self.lf_group,
            textvariable=self.groups_var,
            justify="center",
            state="readonly",
        )
        self.cb_groups.grid(column=1, row=0)
        self.u_window_position()

    def search_window(self):
        """Displays dialog screen for searching."""
        self.show_user_window()
        self.add_label()
        self.add_entry()
        self.add_buttons()
        self.cancel_button.grid(row=3, column=1, pady=(0, 10))
        self.ok_button.grid(row=3, column=0, pady=(0, 10))

        self.cb_search_dir_var = StringVar()
        self.cb_search_dir = ttk.Combobox(
            self.u_window,
            textvariable=self.cb_search_dir_var,
            justify="center",
            state="readonly",
        )

        self.uw_label.configure(text="Search in:")
        self.uw_label.grid(
            row=0,
            column=0,
        )
        self.uw_entry.grid(
            row=2, column=0, columnspan=2, ipady=3, pady=10, padx=20, sticky=NSEW
        )
        self.cb_search_dir.grid(column=0, row=1, columnspan=2, pady=(10, 0))
        self.cb_search_dir.configure(values=["current dir", "home", "all"])
        self.cb_search_dir_var.set("current dir")

        self.u_window_position()
