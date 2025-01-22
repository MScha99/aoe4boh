# gui/tab2.py
import tkinter as tk
from tkinter import ttk

class TemplateTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        # Add widgets and layout for Tab 2
        label = ttk.Label(self, text="template tab")
        label.pack(pady=20)

        entry = ttk.Entry(self)
        entry.pack(pady=10)