from tkinter import *
from tkinter import ttk
from data import sample_build_order
import json
from fuzzywuzzy import process


class BuildOrderEditor:
    def __init__(self, parent, emoticons):
        self.window = Toplevel(parent)
        self.window.title("Build Order Editor")
        self.window.geometry("900x600")
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
                    text_canvas_width = 300
                    text_canvas_height = 180
                    canvas = Canvas(self.table_frame, width=text_canvas_width, height=text_canvas_height, bg="white", bd=0, highlightthickness=0)
                    canvas.grid(column=col, row=row, padx=5, pady=5, sticky=(W, E, N, S))

                    # Insert the instructions into the Canvas
                    instructions = step[key]
                    parts = instructions.split(" ")

                    # Initialize starting positions
                    x_offset = 5  # Starting x position for text/images
                    y_offset = 10  # Starting y position for text/images
                    line_height = 0  # Tracks the height of the current line

                    for part in parts:
                        emoticon_key = f"{part}"
                        if emoticon_key in self.emoticons:
                            # If the part is an emoticon, insert its image into the Canvas
                            emote_image = self.emoticons[emoticon_key]
                            self.image_references.append(emote_image)
                            image_width = 48  # Fixed size for emoticons
                            image_height = 48  # Fixed size for emoticons

                            # Check if the image exceeds the canvas width
                            if x_offset + image_width > text_canvas_width:
                                x_offset = 5  # Move to the next line
                                y_offset += line_height + 5  # Adjust y_offset for the new line
                                line_height = 0  # Reset line height

                            # Draw the image
                            canvas.create_image(x_offset, y_offset, image=emote_image, anchor="nw")
                            x_offset += image_width + 5  # Adjust x_offset for the next item
                            line_height = max(line_height, image_height)  # Update line height

                        else:
                            # If the part is text, insert it into the Canvas
                            text_id = canvas.create_text(x_offset, y_offset, text=part, anchor="nw", font=("Sergoe UI Variable", 26))
                            text_bbox = canvas.bbox(text_id)  # Get the bounding box of the text
                            text_width = text_bbox[2] - text_bbox[0]  # Calculate text width

                            # Check if the text exceeds the canvas width
                            if x_offset + text_width > text_canvas_width:
                                x_offset = 5  # Move to the next line
                                y_offset += line_height + 5  # Adjust y_offset for the new line
                                line_height = 0  # Reset line height

                                # Redraw the text on the new line
                                canvas.delete(text_id)  # Remove the previous text
                                text_id = canvas.create_text(x_offset, y_offset, text=part, anchor="nw", font=("Sergoe UI Variable", 26))
                                text_bbox = canvas.bbox(text_id)  # Get the new bounding box
                                text_width = text_bbox[2] - text_bbox[0]  # Recalculate text width

                            # Adjust x_offset for the next item
                            x_offset += text_width + 5
                            line_height = max(line_height, text_bbox[3] - text_bbox[1])  # Update line height

                    # Bind double-click to open a popup window
                    canvas.bind("<Double-1>", lambda e, r=row, c=col: self.open_popup(r, c))
                else:
                    # Set fixed width for resource columns
                    label = ttk.Label(self.table_frame, text=step[key], anchor="center", width=5)
                    label.grid(column=col, row=row, padx=5, pady=5, sticky=(W, E))
                    label.bind("<Double-1>", lambda e, r=row, c=col: self.edit_cell(r, c))

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
        """Open a Toplevel popup window when the Canvas is double-clicked."""
        if self.active_entry:
            return

        popup = Toplevel(self.window)
        popup.geometry("700x350")
        popup.overrideredirect(True)  # Hide window title bar

        # Center popup on the parent window
        self.window.update_idletasks()
        parent_x = self.window.winfo_x()
        parent_y = self.window.winfo_y()
        parent_width = self.window.winfo_width()
        parent_height = self.window.winfo_height()
        popup_width = 700
        popup_height = 350
        x_position = parent_x + (parent_width - popup_width) // 2
        y_position = parent_y + (parent_height - popup_height) // 2
        popup.geometry(f"{popup_width}x{popup_height}+{x_position}+{y_position}")

        popup.configure(bg="gray30", borderwidth=2, relief="ridge")  # Make it stand out

        # Main popup frame
        popup_frame = ttk.Frame(popup, padding=10)
        popup_frame.pack(fill=BOTH, expand=True)

        # Configure grid weights for popup_frame
        popup_frame.grid_columnconfigure(0, weight=1)  # Text widget column
        popup_frame.grid_columnconfigure(1, weight=0)  # Emoticon frame column (no expansion)
        popup_frame.grid_rowconfigure(0, weight=1)     # Main content row
        popup_frame.grid_rowconfigure(1, weight=0)     # Button row

        # Text widget for instructions
        text_widget = Text(popup_frame, wrap=WORD, width=40, height=10, font=("Sergoe UI Variable", 14))
        text_widget.grid(column=0, row=0, padx=5, pady=5, sticky=(W, E, N, S))

        step = self.build_order[row - 1]
        text_widget.insert(END, step["instructions"])

        def enforce_character_limit(event=None):
            if len(text_widget.get("1.0", END)) > 301:
                text_widget.delete("1.0 + 300 chars", END)

        text_widget.bind("<KeyRelease>", enforce_character_limit)

        # Frame for emoticons with scrollbar
        emoticon_frame = ttk.Frame(popup_frame)
        emoticon_frame.grid(column=1, row=0, padx=5, pady=5, sticky=(N, S))

        # Add a search bar at the top of emoticon_frame
        search_var = StringVar()
        search_entry = ttk.Entry(emoticon_frame, textvariable=search_var, font=("Sergoe UI Variable", 12))
        search_entry.pack(fill=X, padx=5, pady=5)

        # Add a Canvas and Scrollbar to emoticon_frame
        canvas = Canvas(emoticon_frame, width=200, height=250)  # Adjust width and height as needed
        scrollbar = ttk.Scrollbar(emoticon_frame, orient=VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the scrollbar and canvas
        scrollbar.pack(side=RIGHT, fill=Y)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        # Bind mouse scroll wheel to the canvas
        def on_mouse_wheel(event):
            canvas.yview_scroll(-1 * (event.delta // 120), "units")  # For Windows and macOS
            # canvas.yview_scroll(-1 * (event.delta), "units")  # For Linux

        canvas.bind_all("<MouseWheel>", on_mouse_wheel)  # For Windows and macOS

        # Create a frame inside the canvas to hold the emoticon buttons
        inner_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor=NW)

        # Configure the inner frame to update the scroll region
        def update_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        inner_frame.bind("<Configure>", update_scroll_region)

        # Function to update emoticons based on search term
        def update_emoticons(search_term):
            # Clear the inner frame
            for widget in inner_frame.winfo_children():
                widget.destroy()

            # Perform fuzzy search on emoticon keys
            if search_term:
                matches = process.extract(search_term, self.emoticons.keys(), limit=len(self.emoticons))
                filtered_emoticons = {key: self.emoticons[key] for key, score in matches if score > 70}  # Adjust threshold as needed
            else:
                filtered_emoticons = self.emoticons  # Show all emoticons if search term is empty

            # Add filtered emoticon buttons to the inner frame
            row_i = 0
            col_i = 0
            for key, emote_image in filtered_emoticons.items():
                button = ttk.Button(inner_frame, image=emote_image, command=lambda k=key: self.insert_emote(
                    text_widget, k))
                button.grid(column=col_i, row=row_i, padx=2, pady=2, sticky="")
                col_i += 1
                if col_i > 2:
                    col_i = 0
                    row_i += 1
            canvas.yview_moveto(0)

        # Bind the search entry to update emoticons dynamically
        search_var.trace_add("write", lambda *args: update_emoticons(search_var.get()))

        # Initialize with all emoticons
        update_emoticons("")

        # Save and Cancel buttons
        button_frame = ttk.Frame(popup_frame)
        button_frame.grid(column=0, row=1, columnspan=2, pady=10, sticky=(W, E))

        ttk.Button(button_frame, text="Save", command=lambda: self.save_popup_changes(
            row, col, text_widget, popup)).pack(side=LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=lambda: self.close_popup(
            popup)).pack(side=LEFT, padx=5)

        self.active_entry = type(
            "ActiveEntry", (), {"widget": text_widget, "row": row, "col": col})

    def close_popup(self, popup):
        """Close the popup and reset active entry."""
        popup.destroy()
        self.active_entry = None

    def save_popup_changes(self, row, col, text_widget, popup):
        """Save changes from the popup and close it."""
        step = self.build_order[row - 1]
        step["instructions"] = text_widget.get("1.0", END).strip()
        self.populate_table()
        self.close_popup(popup)

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

    def show_emote_menu(self, text_widget):
        """Show a popup menu with emoticons."""
        self.emote_menu = Toplevel(self.window)
        self.emote_menu.title("Select Emote")
        self.emote_menu.geometry("200x100")
        self.emote_menu.transient(self.window)  # Attach to the main window

        # Add emoticons to the menu
        for key, emote_image in self.emoticons.items():
            emote_button = ttk.Button(self.emote_menu, image=emote_image,
                                      command=lambda k=key: self.insert_emote(text_widget, k))
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
        text_widget.insert(
            # Insert the emote key in the correct format
            "insert", f"{emote_key}")
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
