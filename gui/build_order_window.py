from tkinter import *
from tkinter import ttk, messagebox
import customtkinter
from data import sample_build_order
import json
from fuzzywuzzy import process
from .instructions_renderer import InstructionsRenderer
from .text_editor_popup import TextEditorPopup


class BuildOrderEditor:
    def __init__(self, parent, emoticons, build_file):
        self.window = Toplevel(parent)
        self.window.title("Build Order Editor")
        self.window.geometry("900x600")
        self.build_order = None
        self.emoticons = emoticons
        self.window.configure(bg="#33393b")
        self.instructions_width = 300
        self.instructions_height = 180
        self.build_file = build_file
        self.active_entry = None
        self.emote_menu = None
        self.image_references = []

        if not self.load_build_order():
            return
        self.text_editor_popup = TextEditorPopup(
            self.window, self.emoticons, self.build_order, self)
        self.create_widgets()

    def create_widgets(self):
        # Title label
        ttk.Label(self.window, text="Build Order Editor").grid(
            column=0, row=0, columnspan=8, pady=10
        )

        # Save and Load buttons
        ttk.Button(self.window, text="Save", command=self.save_build_order).grid(
            column=0, row=1, sticky=(E), padx=5, pady=5
        )
        ttk.Button(self.window, text="Quit", command=lambda: self.window.destroy()).grid(
            column=1, row=1, sticky=(W, E), padx=5, pady=5
        )

        # Frame to hold the table
        # self.table_frame = ttk.Frame(self.window)
        self.table_frame = customtkinter.CTkScrollableFrame(self.window, fg_color="#33393b")
        self.table_frame.grid(column=0, row=2, columnspan=8,
                              sticky=(W, E, N, S), padx=10, pady=10)

        # Define headers
        headers = ["Actions", "Index", "Instructions",
                   "Food", "Wood", "Gold", "Stone", "Move"]
        for col, header in enumerate(headers):
            ttk.Label(self.table_frame, text=header, font=("Sergoe UI Variable", 14, "bold")).grid(
                column=col, row=0, padx=5, pady=5, sticky=(W, E)
            )

        # Populate the table with the build order
        self.populate_table()

        # Configure grid weights for resizing
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(2, weight=1)

    def populate_table(self):
        """Populate the table with the current build order."""
        # Clear existing rows and image references
        for widget in self.table_frame.winfo_children():
            if int(widget.grid_info()["row"]) > 0:  # Skip header row
                widget.destroy()
        self.image_references.clear()

        # Add rows for each step
        for row, step in enumerate(self.build_order, start=1):
            # Add - button for each row
            ttk.Button(self.table_frame, text="-", width=2,
                       command=lambda r=row: self.remove_step(r)).grid(column=0, row=row, padx=5, pady=5)

            # Add index column
            ttk.Label(self.table_frame, text=str(row), anchor="center").grid(
                column=1, row=row, padx=5, pady=5, sticky=(W, E)
            )

            # Add step details (editable labels)
            for col, key in enumerate(["instructions", "desired_food_workers", "desired_wood_workers", "desired_gold_workers", "desired_stone_workers"], start=2):
                if key == "instructions":
                    canvas = Canvas(self.table_frame, width=self.instructions_width,
                                    height=self.instructions_height, bg='white', bd=0, highlightthickness=0)
                    canvas.grid(column=col, row=row, padx=5,
                                pady=5, sticky=(W, E, N, S))

                    def double_click_callback(
                        e, r=row, c=col): return self.open_popup(r, c)
                    instructions_renderer = InstructionsRenderer(
                        canvas, self.emoticons, self.instructions_width, double_click_callback)
                    instructions_renderer.render_text_with_emoticons(step[key])
                else:
                    # Set fixed width for resource columns
                    label = ttk.Label(self.table_frame,
                                      text=step[key], anchor="center", width=5)
                    label.grid(column=col, row=row, padx=5,
                               pady=5, sticky=(W, E))
                    label.bind("<Double-1>", lambda e, r=row,
                               c=col: self.edit_cell(r, c))

                    # Highlight on hover (restored logic)
                    label.bind("<Enter>", lambda e,
                               l=label: l.configure(background="lightgray"))
                    label.bind("<Leave>", lambda e,
                               l=label: l.configure(background=""))

            # Add up/down arrows for moving rows
            button_frame = ttk.Frame(self.table_frame)
            button_frame.grid(column=7, row=row, padx=5, pady=5)

            if row > 1:
                ttk.Button(button_frame, text="▲", style="Small.TButton",
                           command=lambda r=row: self.move_row_up(r)).pack(side=TOP, pady=1)
            else:
                ttk.Label(button_frame, text="").pack(side=TOP, pady=1)

            if row < len(self.build_order):
                ttk.Button(button_frame, text="▼", style="Small.TButton",
                           command=lambda r=row: self.move_row_down(r)).pack(side=TOP, pady=1)
            else:
                ttk.Label(button_frame, text="").pack(side=TOP, pady=1)

        # Add + button in the last row
        add_row = len(self.build_order) + 1
        ttk.Button(self.table_frame, text="+", width=2,
                   command=lambda: self.add_step(add_row)).grid(column=0, row=add_row, padx=5, pady=5)

    def open_popup(self, row, col):
        """Open a popup window for editing instructions."""
        self.text_editor_popup.open_popup(row, col)

    def edit_cell(self, row, col):
        """Handle double-click events to make cells editable."""
        if self.active_entry:
            # If another cell is being edited, do nothing
            return

        # Get the current value of the cell
        step = self.build_order[row - 1]
        keys = ["instructions", "desired_food_workers", "desired_wood_workers",
                "desired_gold_workers", "desired_stone_workers"]
        current_value = step[keys[col - 2]]

        # Create a Text widget for editing if it's the Instructions column
        if keys[col - 2] == "instructions":
            text_widget = Text(self.table_frame, wrap=WORD,
                               width=30, height=3, font=("Sergoe UI Variable", 14))
            text_widget.insert(END, current_value)
            text_widget.grid(column=col, row=row, padx=5,
                             pady=5, sticky=(W, E, N, S))
            text_widget.focus()

            # Add an emote button next to the Text widget
            emote_button = ttk.Button(
                self.table_frame, text="😀", command=lambda: self.show_emote_menu(text_widget))
            emote_button.grid(column=col + 1, row=row,
                              padx=5, pady=5, sticky=(W, E))

            # Save the edited value when the user presses Enter
            text_widget.bind("<Return>", lambda e, r=row, c=col,
                             tw=text_widget: self.save_edit(r, c, tw))

            # Track the active Text widget
            self.active_entry = type(
                "ActiveEntry", (), {"widget": text_widget, "row": row, "col": col})
        else:
            # Create an Entry widget for editing resource fields
            entry = ttk.Entry(self.table_frame, font=(
                "Sergoe UI Variable", 14))  # Match the font size
            entry.configure(width=5)  # Adjust width as needed
            entry.insert(0, current_value)
            entry.select_range(0, END)
            entry.focus()

            # Validate input for resource fields (only integers allowed, max 2 digits)
            entry.configure(validate="key")
            entry.configure(validatecommand=(
                entry.register(self.validate_integer), "%P"))

            # Place the Entry widget using grid
            entry.grid(column=col, row=row, padx=5, pady=5, sticky=(W, E))

            # Save the edited value when the user presses Enter
            entry.bind("<Return>", lambda e, r=row, c=col,
                       en=entry: self.save_edit(r, c, en))

            # Track the active Entry widget
            self.active_entry = type(
                "ActiveEntry", (), {"widget": entry, "row": row, "col": col})

    def validate_integer(self, value):
        """Validate that the input is an integer and no more than 2 digits."""
        if value == "":
            return True  # Allow empty input
        try:
            int_value = int(value)
            return 0 <= int_value <= 99  # Only allow 2-digit numbers
        except ValueError:
            return False

    def save_edit(self, row, col, widget):
        """Save the edited value back to the build_order."""
        if isinstance(widget, Text):
            # Get text from Text widget
            new_value = widget.get("1.0", END).strip()
            widget.destroy()  # Remove the Text widget
        else:
            new_value = widget.get()  # Get text from Entry widget
            widget.destroy()  # Remove the Entry widget

        self.active_entry = None  # Clear the active widget

        # Update the build_order data
        step = self.build_order[row - 1]
        keys = ["instructions", "desired_food_workers", "desired_wood_workers",
                "desired_gold_workers", "desired_stone_workers"]
        step[keys[col - 2]] = new_value  # Adjust for actions and index columns

        # Refresh the table
        self.populate_table()

    def add_step(self, row):
        """Add a new step after the selected row."""
        new_step = {
            "instructions": "New Step",
            "desired_food_workers": 0,
            "desired_wood_workers": 0,
            "desired_gold_workers": 0,
            "desired_stone_workers": 0
        }
        self.build_order.insert(row, new_step)
        self.populate_table()  # Refresh the table

    def remove_step(self, row):
        """Remove the selected step."""
        self.build_order.pop(row - 1)  # Adjust for 0-based index
        self.populate_table()  # Refresh the table

    def move_row_up(self, row):
        """Move the selected row up."""
        if row > 1:
            self.build_order[row - 1], self.build_order[row -
                                                        2] = self.build_order[row - 2], self.build_order[row - 1]
            self.populate_table()  # Refresh the table

    def move_row_down(self, row):
        """Move the selected row down."""
        if row < len(self.build_order):
            self.build_order[row -
                             1], self.build_order[row] = self.build_order[row], self.build_order[row - 1]
            self.populate_table()  # Refresh the table

    def save_build_order(self):
        """Save the build order to a JSON file specified in self.build_file."""
        with open(self.build_file, "w") as file:
            json.dump(self.build_order, file, indent=4)
        self.populate_table()

    def load_build_order(self):
        """Load the build order from a JSON file."""
        try:
            with open(self.build_file, "r") as file:
                self.build_order = json.load(file)
                return True
                # self.populate_table()  # Refresh the table
        except FileNotFoundError:
            self.window.destroy()
            messagebox.showerror("Error", "this file does not exist")
            return False

        except (FileNotFoundError, json.JSONDecodeError) as e:
            # Display an error message in a dialog box
            self.window.destroy()
            messagebox.showerror(
                "Error", f"Failed to load the build order, your build order file might be corrupted or written improperly.\n\n{str(e)}")
            return False
