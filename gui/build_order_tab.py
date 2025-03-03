from tkinter import *
from tkinter import ttk, messagebox, simpledialog
from .build_order_window import BuildOrderEditor
import os
import json
from datetime import datetime
from data import civs


class BuildOrderTab(ttk.Frame):
    def __init__(self, parent, settings, emoticons, base_dir="build_orders"):
        super().__init__(parent)
        self.settings = settings
        self.emoticons = emoticons
        self.civs = civs
        self.base_dir = base_dir
        self.selected_build_order_name = None
        self.create_widgets()
        self.set_default_values()

    def create_widgets(self):
        # === Configure Grid Layout ===
        self.grid_columnconfigure(0, weight=1, uniform="equal")
        self.grid_columnconfigure(1, weight=1, uniform="equal")
        self.grid_columnconfigure(2, weight=1, uniform="equal")
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=0)
        self.grid_rowconfigure(5, weight=0)

        # === Main Label ===
        self.label = ttk.Label(self, text="Build Order Tab")
        self.label.grid(column=0, row=0, columnspan=3, pady=10)

        # === Civilization Combobox ===
        self.civ_combobox = ttk.Combobox(
            self,
            state="readonly",
            values=list(self.civs.keys()),
            font=('TkDefaultFont', 11)
        )
        self.civ_combobox.grid(
            column=0, row=1, columnspan=2, padx=(50, 0), pady=10, sticky=(W, E))
        self.civ_combobox.bind("<<ComboboxSelected>>", self.on_civ_select)

        # === Flag Label ===
        self.flag_label = ttk.Label(self)
        self.flag_label.grid(column=2, row=1, padx=(0, 10), pady=10, sticky="")

        # === Build Order Listbox ===
        self.build_order_list = Listbox(self)
        self.build_order_list.grid(
            column=0, row=2, columnspan=3, rowspan=4, pady=10, padx=10, sticky=(W, E, N, S))
        self.build_order_list.bind(
            '<<ListboxSelect>>', self.on_build_order_select)
        self.build_order_list.bind(
            '<Double-Button-1>', self.on_build_order_double_click)

        # === Action Buttons ===
        # Create a frame for buttons
        button_frame = ttk.Frame(self,)
        button_frame.grid(column=3, row=2, rowspan=4, sticky=(N, S), pady=10)

        # Add buttons to the frame
        self.add_button = ttk.Button(
            button_frame, text="Add", command=self.create_new_build, state=NORMAL)
        self.add_button.pack(fill='x', pady=5)

        self.edit_button = ttk.Button(
            button_frame, text="Edit", command=self.edit_build_order, state=DISABLED)
        self.edit_button.pack(fill='x', pady=5)

        self.delete_button = ttk.Button(
            button_frame, text="Delete", command=self.delete_build_order, state=DISABLED)
        self.delete_button.pack(fill='x', pady=5)

        self.rename_button = ttk.Button(
            button_frame, text="Rename", command=self.rename_build_order, state=DISABLED)
        self.rename_button.pack(fill='x', pady=5)

        self.set_active_button = ttk.Button(
            button_frame, text="Set Active", command=self.set_active_build_order, state=DISABLED)
        self.set_active_button.pack(fill='x', pady=5)

    def set_active_build_order(self):
        """Set the selected build order as the active build order."""
        selected_indices = self.build_order_list.curselection()
        if selected_indices:
            self.selected_build_order_name = self.build_order_list.get(
                selected_indices[0])
            build_file = self.get_build_file_path(
                self.selected_build_order_name)
            self.settings.active_build_order = build_file
            selected_civ=self.civ_combobox.get()
            self.populate_build_order_list(selected_civ)
        

    def set_default_values(self):
        """Set default values for the UI."""
        civ_keys = list(self.civs.keys())
        if civ_keys:
            default_civ = civ_keys[0]
            self.civ_combobox.set(default_civ)
            self.display_flag(self.civs[default_civ]["flag"])
            self.populate_build_order_list(default_civ)

    def on_civ_select(self, event):
        """Handle the selection of a civilization in the combobox."""
        selected_civ = self.civ_combobox.get()
        if selected_civ:
            self.display_flag(self.civs[selected_civ]["flag"])
            self.populate_build_order_list(selected_civ)

    def populate_build_order_list(self, civ_name):
        """Populate the build order list based on the selected civilization."""
        self.build_order_list.delete(0, END)  # Clear existing items
        civ_dir = os.path.join(self.base_dir, civ_name)
        if os.path.exists(civ_dir):
            active_build_order = self.settings.active_build_order
            active_build_name = None

            # Extract the active build order name (without the path) if it exists
            if active_build_order:
                active_build_name = os.path.basename(
                    active_build_order).rsplit("_build.json", 1)[0]

            for filename in os.listdir(civ_dir):
                if filename.endswith("_build.json"):
                    build_order_name = filename.rsplit("_build.json", 1)[0]
                    if active_build_name == build_order_name:
                        # Highlight the active build order with >>> <<< symbols
                        display_name = f">>> {build_order_name} <<<"
                    else:
                        display_name = build_order_name
                    self.build_order_list.insert(END, display_name)

    def display_flag(self, flag_key):
        """Display the flag corresponding to the selected civilization."""
        flag_image = self.emoticons.get(flag_key)
        self.flag_label.config(image=flag_image if flag_image else "")

    def on_build_order_select(self, event):
        """Handle the selection of a build order in the listbox."""
        selected_indices = self.build_order_list.curselection()
        if selected_indices:
            self.selected_build_order_name = self.build_order_list.get(
                selected_indices[0])
            self.update_button_states(True)
        else:
            self.selected_build_order_name = None
            self.update_button_states(False)

    def on_build_order_double_click(self, event):
        """Handle the double-click event on a build order in the listbox."""
        self.set_active_build_order()

    def update_button_states(self, enable):
        """Enable or disable the Edit and Delete buttons."""
        state = NORMAL if enable else DISABLED
        self.edit_button.config(state=state)
        self.delete_button.config(state=state)
        self.rename_button.config(state=state)
        self.set_active_button.config(state=state)

    def get_build_file_path(self, build_order_name):
        """Get the full path to a build order file."""
        selected_civ = self.civ_combobox.get()
        return os.path.join(self.base_dir, selected_civ, f"{build_order_name}_build.json")

    def edit_build_order(self):
        """Open the BuildOrderEditor with the selected build order."""
        if self.selected_build_order_name:
            build_file = self.get_build_file_path(
                self.selected_build_order_name)
            BuildOrderEditor(self, self.emoticons, build_file=build_file)

    def create_new_build(self):
        """Create a new build order."""
        default_build_order = [
            {
                "instructions": "New Step",
                "desired_food_workers": 0,
                "desired_wood_workers": 0,
                "desired_gold_workers": 0,
                "desired_stone_workers": 0
            }
        ]
        selected_civ = self.civ_combobox.get()
        timestamp = datetime.now().strftime("%m%d%H%M%S")
        build_name = f"new_build_{timestamp}"
        build_file = self.get_build_file_path(build_name)
        with open(build_file, "w") as f:
            json.dump(default_build_order, f)
        self.populate_build_order_list(selected_civ)

    def delete_build_order(self):
        """Delete the selected build order."""
        if self.selected_build_order_name:
            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete '{
                    self.selected_build_order_name}'?"
            )
            if confirm:
                build_file = self.get_build_file_path(
                    self.selected_build_order_name)
                os.remove(build_file)
                self.populate_build_order_list(self.civ_combobox.get())

    def rename_build_order(self):
        """Prompt the user to rename the selected build order."""
        if self.selected_build_order_name:
            current_name = self.selected_build_order_name
            new_name = simpledialog.askstring(
                "Rename Build Order", "Enter a new name:", initialvalue=current_name, parent=self
            )

            if new_name and new_name.strip() != current_name:
                success = self.perform_rename(current_name, new_name.strip())
                if success:
                    self.populate_build_order_list(
                        self.civ_combobox.get())  # Refresh the list

    def perform_rename(self, old_name, new_name):
        """Rename the build order file and handle errors."""
        selected_civ = self.civ_combobox.get()
        old_file = self.get_build_file_path(old_name)
        new_file = self.get_build_file_path(new_name)

        if os.path.exists(old_file):
            try:
                os.rename(old_file, new_file)
                print(f"Renamed '{old_name}' to '{new_name}'.")
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Failed to rename file: {e}")
        else:
            messagebox.showerror("Error", f"File '{old_name}' does not exist.")
        return False
