# gui/main_window.py
from tkinter import *
from tkinter import ttk, font
from .ocr_tab import OcrTab
from .template_tab import TemplateTab
import os


class MainWindow:
    def __init__(self, root, settings, controller):
        self.root = root
        self.settings=settings
        self.controller=controller
        self.root.title("AoE4 build order helper")

        self.root.geometry('500x500')  # default window size        
        self.center_window()
        self.setup_ui()

    def setup_ui(self):
        # setup theme
        base_path = os.path.dirname(__file__)
        theme_path = os.path.join(base_path, "awthemes-10.4.0")
        self.root.tk.call("lappend", "auto_path", theme_path)       
        self.root.tk.call("package", "require", "awdark")
        style = ttk.Style()
        style.theme_use("awdark")

        # create a frame in root window, that allows for resizing and uses grid to manage layout
        mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        # change default font
        self.defaultFont = font.nametofont("TkDefaultFont")
        self.defaultFont.configure(family="Sergoe UI Variable",
                                   size=14)
        # Create a Notebook widget
        notebook = ttk.Notebook(self.root)
        notebook.grid(column=0, row=0, sticky=(N, W, E, S), padx=5)

        # Create instances of each tab
        tab1 = OcrTab(notebook, self.settings, self.controller)
        tab2 = TemplateTab(notebook)
        tab1.configure(padding=20)
        tab2.configure(padding=20)

        # Add tabs to the notebook
        notebook.add(tab1, text="OCR")
        notebook.add(tab2, text="Templates")


    def center_window(self):
        """
        Center the window on the screen.
        """
        # Update the window to ensure accurate dimensions
        self.root.update_idletasks()

        # Get the screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Get the window dimensions
        window_width = self.root.winfo_reqwidth()
        window_height = self.root.winfo_reqheight()

        # Calculate the position to center the window
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        # Set the window geometry
        self.root.geometry(f'+{x_position}+{y_position}')
