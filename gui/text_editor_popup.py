from tkinter import *
from tkinter import ttk
from fuzzywuzzy import process
import customtkinter


class TextEditorPopup:
    def __init__(self, parent, emoticons, build_order, build_order_editor):
        """
        Initialize the PopupManager.
        Args:
            parent (tk.Toplevel): The parent window.
            emoticons (dict): A dictionary mapping emoticon keys to their corresponding images.
            build_order_manager (BuildOrderManager): The manager for build order data.
        """
        self.parent = parent
        self.emoticons = emoticons
        self.build_order = build_order
        self.build_order_editor = build_order_editor
        self.active_entry = None

    def open_popup(self, row, col):
        """Open a Toplevel popup window when the Canvas is double-clicked."""
        if self.active_entry:
            return

        popup = Toplevel(self.parent)
        popup.geometry("700x350")
        popup.overrideredirect(True)  # Hide window title bar

        # Center popup on the parent window
        self.parent.update_idletasks()
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        popup_width = 700
        popup_height = 350
        x_position = parent_x + (parent_width - popup_width) // 2
        y_position = parent_y + (parent_height - popup_height) // 2
        popup.geometry(f"{popup_width}x{
                       popup_height}+{x_position}+{y_position}")
        popup.configure(bg="#33393b", borderwidth=2, relief="ridge")

        # Main popup frame
        popup_frame = ttk.Frame(popup, padding=10)
        popup_frame.pack(fill=BOTH, expand=True)

        # Configure grid weights for popup_frame
        popup_frame.grid_columnconfigure(0, weight=1)  # Text widget column
        # Emoticon frame column (no expansion)
        popup_frame.grid_columnconfigure(1, weight=0)
        popup_frame.grid_rowconfigure(0, weight=1)     # Main content row
        popup_frame.grid_rowconfigure(1, weight=0)     # Button row

        # Text widget for instructions
        text_widget = Text(popup_frame, wrap=WORD, width=40,
                           height=10, font=("Sergoe UI Variable", 14))
        text_widget.grid(column=0, row=0, padx=5, pady=5, sticky=(W, E, N, S))

        step = self.build_order[row - 1]
        text_widget.insert(END, step["instructions"])

        def enforce_character_limit(event=None):
            if len(text_widget.get("1.0", END)) > 301:
                text_widget.delete("1.0 + 300 chars", END)

        text_widget.bind("<KeyRelease>", enforce_character_limit)

        # Frame for emoticons with CTkScrollableFrame
        emoticon_frame = ttk.Frame(popup_frame)
        emoticon_frame.grid(column=1, row=0, padx=5, pady=5, sticky=(N, S))

        # Add a search bar at the top of emoticon_frame
        search_var = StringVar()
        search_entry = ttk.Entry(
            emoticon_frame, textvariable=search_var, font=("Sergoe UI Variable", 12))
        search_entry.pack(fill=X, padx=5, pady=5)

        # Create a CTkScrollableFrame to hold the emoticon buttons
        scrollable_frame = customtkinter.CTkScrollableFrame(
            emoticon_frame, width=200, height=250, fg_color="#33393b")
        scrollable_frame.pack(fill=BOTH, expand=True)

        # Function to update emoticons based on search term
        def update_emoticons(search_term):
            # Clear the scrollable frame
            for widget in scrollable_frame.winfo_children():
                widget.destroy()

            # Perform fuzzy search on emoticon keys
            if search_term:
                matches = process.extract(
                    search_term, self.emoticons.keys(), limit=len(self.emoticons))
                # Adjust threshold as needed
                filtered_emoticons = {
                    key: self.emoticons[key] for key, score in matches if score > 70}
            else:
                filtered_emoticons = self.emoticons  # Show all emoticons if search term is empty

            # Add filtered emoticon buttons to the scrollable frame
            row_i = 0
            col_i = 0
            for key, emote_image in filtered_emoticons.items():
                button = ttk.Button(
                    scrollable_frame, image=emote_image, command=lambda k=key: self.insert_emote(
                        text_widget, k)
                )
                button.grid(column=col_i, row=row_i, padx=2, pady=2, sticky="")
                col_i += 1
                if col_i > 2:
                    col_i = 0
                    row_i += 1

            # Reset the scrollbar to the top
            # Access the internal canvas and reset its view
            scrollable_frame._parent_canvas.yview_moveto(0)

        # Bind the search entry to update emoticons dynamically
        search_var.trace_add(
            "write", lambda *args: update_emoticons(search_var.get()))

        # Initialize with all emoticons
        update_emoticons("")

        # Save and Cancel buttons
        button_frame = ttk.Frame(popup_frame)
        button_frame.grid(column=0, row=1, columnspan=2,
                          pady=10, sticky=(W, E))

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
        self.close_popup(popup)
        self.build_order_editor.populate_table()

    def insert_emote(self, text_widget, emote_key):
        """Insert the selected emote into the Text widget."""
        text_widget.insert("insert", f"{emote_key}")
        text_widget.focus()  # Return focus to the Text widget
