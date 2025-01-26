from tkinter import *
from tkinter import ttk
from .build_order_window import BuildOrderEditor


class BuildOrderTab(ttk.Frame):
    def __init__(self, parent, emoticons):
        super().__init__(parent)
        self.create_widgets()
        self.emoticons = emoticons

    def create_widgets(self):
        # Label
        self.label = ttk.Label(self, text="Build Order Tab")
        self.label.grid(column=0, row=0, columnspan=2, pady=10)

        # Listbox to display build orders
        self.build_order_list = Listbox(self)
        self.build_order_list.grid(
            column=0, row=1, columnspan=2, pady=10, padx=10, sticky=(W, E, N, S))

        # Add button
        self.add_button = ttk.Button(
            self, text="Add Build Order", command=lambda: BuildOrderEditor(self, self.emoticons)
        )
        self.add_button.grid(column=0, row=2, columnspan=2, pady=5)

        # Configure grid weights for resizing
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
