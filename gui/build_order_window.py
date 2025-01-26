from tkinter import *
from tkinter import ttk
from data import sample_build_order
import json

class BuildOrderEditor:
    def __init__(self, parent, emoticons):
        self.window = Toplevel(parent)
        self.window.title("Build Order Editor")
        self.window.geometry("700x600")
        self.build_order = sample_build_order
        self.emoticons = emoticons
        self.window.configure(bg="gray20")

        self.filename = "testowy"
        self.active_entry = None
        self.emote_menu = None
        self.image_references = []
        self.create_widgets()

    def create_widgets(self):
        # Title label
        ttk.Label(self.window, text="Build Order Editor").grid(
            column=0, row=0, columnspan=8, pady=10
        )

        # Save and Load buttons
        ttk.Button(self.window, text="Save", command=self.save_build_order).grid(
            column=0, row=1, sticky=(W, E), padx=5, pady=5
        )
        ttk.Button(self.window, text="Load", command=self.load_build_order).grid(
            column=1, row=1, sticky=(W, E), padx=5, pady=5
        )

        # Frame to hold the table
        self.table_frame = ttk.Frame(self.window)
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
                    # Create a Canvas widget for the instructions column
                    canvas = Canvas(self.table_frame, width=200, height=60, bg="white", bd=0, highlightthickness=0)
                    canvas.grid(column=col, row=row, padx=5, pady=5, sticky=(W, E, N, S))

                    # Insert the instructions into the Canvas
                    instructions = step[key]
                    parts = instructions.split("::")
                    x_offset = 5  # Starting x position for text/images
                    for part in parts:
                        emoticon_key = f":{part}:"
                        if emoticon_key in self.emoticons:
                            # If the part is an emote, insert its image into the Canvas
                            emote_image = self.emoticons[emoticon_key]
                            self.image_references.append(emote_image)
                            canvas.create_image(x_offset, 10, image=emote_image, anchor="nw")
                            x_offset += emote_image.width() + 5  # Adjust x offset for the next item
                        else:
                            # If the part is text, insert it into the Canvas
                            text_id = canvas.create_text(x_offset, 10, text=part, anchor="nw", font=("Sergoe UI Variable", 14))
                            x_offset += canvas.bbox(text_id)[2] - canvas.bbox(text_id)[0] + 5  # Adjust x offset for the next item

                    # Bind double-click to open a popup window
                    canvas.bind("<Double-1>", lambda e, r=row, c=col: self.open_popup(r, c))
                else:
                    # Set fixed width for resource columns
                    label = ttk.Label(self.table_frame,
                                    text=step[key], anchor="center", width=5)
                    label.grid(column=col, row=row, padx=5,
                            pady=5, sticky=(W, E))
                    label.bind("<Double-1>", lambda e, r=row,
                            c=col: self.edit_cell(r, c))

                    # Highlight on hover (restored logic)
                    label.bind("<Enter>", lambda e, l=label: l.configure(background="lightgray"))
                    label.bind("<Leave>", lambda e, l=label: l.configure(background=""))

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

    # Rest of the methods remain unchanged...

    def open_popup(self, row, col):
        """Open a Toplevel popup window when the Text widget is double-clicked."""
        popup = Toplevel(self.window)
        popup.title("Edit Instructions")
        popup.geometry("400x300")

        # Add a Text widget to the popup
        text_widget = Text(popup, wrap=WORD, width=40, height=10, font=("Sergoe UI Variable", 14))
        text_widget.pack(padx=10, pady=10)

        # Insert the current instructions into the Text widget
        step = self.build_order[row - 1]
        text_widget.insert(END, step["instructions"])

        # Add Save and Cancel buttons
        button_frame = ttk.Frame(popup)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Save", command=lambda: self.save_popup_changes(row, col, text_widget, popup)).pack(side=LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=popup.destroy).pack(side=LEFT, padx=5)

    def save_popup_changes(self, row, col, text_widget, popup):
        """Save changes from the popup and close it."""
        step = self.build_order[row - 1]
        step["instructions"] = text_widget.get("1.0", END).strip()
        self.populate_table()  # Refresh the table
        popup.destroy()


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
            emote_button = ttk.Button(self.table_frame, text="😀", command=lambda: self.show_emote_menu(text_widget))
            emote_button.grid(column=col + 1, row=row, padx=5, pady=5, sticky=(W, E))

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

    def show_emote_menu(self, text_widget):
        """Show a popup menu with emoticons."""
        self.emote_menu = Toplevel(self.window)
        self.emote_menu.title("Select Emote")
        self.emote_menu.geometry("200x100")
        self.emote_menu.transient(self.window)  # Attach to the main window

        # Add emoticons to the menu
        for key, emote_image in self.emoticons.items():
            emote_button = ttk.Button(self.emote_menu, image=emote_image, command=lambda k=key: self.insert_emote(text_widget, k))
            emote_button.pack(side="top", padx=5, pady=5)

        # Close the menu when clicking outside
        self.emote_menu.bind("<FocusOut>", lambda e: self.close_emote_menu())

    def close_emote_menu(self):
        """Close the emote menu."""
        if self.emote_menu:
            self.emote_menu.destroy()
            self.emote_menu = None

    def insert_emote(self, text_widget, emote_key):
        """Insert the selected emote into the Text widget."""
        text_widget.insert("insert", f":{emote_key}:")  # Insert the emote key in the correct format
        text_widget.focus()  # Return focus to the Text widget
        self.close_emote_menu()  # Close the emote menu after inserting

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
        """Save the build order to a JSON file."""
        with open(self.filename + "_build.json", "w") as file:
            json.dump(self.build_order, file, indent=4)

    def load_build_order(self):
        """Load the build order from a JSON file."""
        with open(self.filename + "_build.json", "r") as file:
            self.build_order = json.load(file)
            self.populate_table()  # Refresh the table