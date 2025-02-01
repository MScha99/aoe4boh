from tkinter import *
from tkinter import ttk
from .build_order_window import BuildOrderEditor
import os
from data import civs


class BuildOrderTab(ttk.Frame):
    def __init__(self, parent, emoticons, base_dir="build_orders"):
        super().__init__(parent)
        self.emoticons = emoticons
        self.civs = civs
        self.base_dir = base_dir
        self.create_widgets()
        self.set_default_values()

    def create_widgets(self):
        # Label
        self.label = ttk.Label(self, text="Build Order Tab")
        self.label.grid(column=0, row=0, columnspan=3, pady=10)

        # Combobox to select civilization
        self.civ_combobox = ttk.Combobox(
            self,
            state="readonly",
            values=list(self.civs.keys()),
            width=20,
            font=('TkDefaultFont', 11)
        )
        self.civ_combobox.grid(column=0, row=1, padx=10,
                               pady=10, sticky=(W, E))
        self.civ_combobox.bind("<<ComboboxSelected>>", self.on_civ_select)

        # Label to display the flag
        # Store the label in an instance variable
        self.flag_label = ttk.Label(self)
        self.flag_label.grid(column=1, row=1, padx=10, pady=10, sticky=(W, E))

        # Listbox to display build orders
        # Store the listbox in an instance variable
        self.build_order_list = Listbox(self)
        self.build_order_list.grid(
            column=0, row=2, columnspan=3, pady=10, padx=10, sticky=(W, E, N, S))
        self.build_order_list.bind(
            '<<ListboxSelect>>', self.on_build_order_select)

        # Add button (disabled initially)
        self.add_button = ttk.Button(
            self,
            text="Edit Build Order",
            command=lambda: self.open_build_order_editor(),
            state=DISABLED  # Initially disabled
        )
        self.add_button.grid(column=0, row=3, columnspan=3, pady=5)

        # Configure grid weights for resizing
        self.grid_columnconfigure(0, weight=1)
        # Adjust row configuration for the listbox
        self.grid_rowconfigure(2, weight=1)

        # Store the currently selected build order name
        self.selected_build_order_name = None

    def on_civ_select(self, event):
        """Handle the selection of a civilization in the combobox."""
        selected_civ = self.civ_combobox.get()
        if selected_civ:
            flag_key = self.civs[selected_civ]["flag"]
            self.display_flag(flag_key)
            self.populate_build_order_list(selected_civ)

    def populate_build_order_list(self, civ_name, base_dir=None):
        """Populate the build order list based on the selected civilization."""
        self.build_order_list.delete(0, END)  # Clear existing items
        civ_dir = os.path.join(
            self.base_dir, civ_name) if base_dir is None else os.path.join(base_dir, civ_name)
        if os.path.exists(civ_dir):
            for filename in os.listdir(civ_dir):
                if filename.endswith("_build.json"):
                    # Remove the "_build.json" suffix to get the build order name
                    build_order_name = filename.rsplit("_build.json", 1)[0]
                    self.build_order_list.insert(END, build_order_name)

    def display_flag(self, flag_key):
        """Display the flag corresponding to the selected civilization."""
        flag_image = self.emoticons.get(flag_key)
        if flag_image:
            self.flag_label.config(image=flag_image)
        else:
            # Clear the label if no image found
            self.flag_label.config(image='')

    def set_default_values(self):
        civ_keys = list(self.civs.keys())
        # default selected civ with its flag for the first launch
        if civ_keys:
            default_civ = civ_keys[0]
            self.civ_combobox.set(default_civ)
            self.display_flag(self.civs[default_civ]["flag"])
            self.populate_build_order_list(default_civ)

    def on_build_order_select(self, event):
        """Handle the selection of a build order in the listbox."""
        selected_indices = self.build_order_list.curselection()
        if selected_indices:
            selected_index = selected_indices[0]
            self.selected_build_order_name = self.build_order_list.get(
                selected_index)
            # Enable the button and update its command
            self.add_button.config(
                state=NORMAL, command=lambda: self.open_build_order_editor())
        else:
            # Disable the button if nothing is selected
            self.add_button.config(state=DISABLED)
            self.selected_build_order_name = None

    def open_build_order_editor(self):
        """Open the BuildOrderEditor with the selected build order name including directory."""
        if self.selected_build_order_name:
            selected_civ = self.civ_combobox.get()
            build_file = f"build_orders\\{selected_civ}\\{
                self.selected_build_order_name}_build.json"
            BuildOrderEditor(self, self.emoticons, build_file=build_file)
