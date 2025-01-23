# gui/ocr_tab.py
from tkinter import *
from tkinter import ttk
import cv2
import threading
import queue
from ocr import OCRProcessor
from screencap import capture_window
from controller import Controller


class OcrTab(ttk.Frame):
    def __init__(self, parent, consecutive_readings=3):
        super().__init__(parent)
        self.controller = Controller(consecutive_readings)
        self.debug_static_image_var = BooleanVar(
            value=self.controller.debug_static_image)
        self.setup_ui()
        self.start_gui_update_loop()

    def setup_ui(self):
        # Define StringVars for each label
        self.population = StringVar()
        self.idle_workers = StringVar()
        self.food_workers = StringVar()
        self.wood_workers = StringVar()
        self.gold_workers = StringVar()
        self.stone_workers = StringVar()

        # Create labels and associate them with StringVars
        ttk.Label(self, text="Populacja").grid(column=1, row=2, sticky=(W, E))
        ttk.Label(self, textvariable=self.population).grid(
            column=2, row=2, sticky=(W, E))

        ttk.Label(self, text="Idle Workers").grid(
            column=1, row=3, sticky=(W, E))
        ttk.Label(self, textvariable=self.idle_workers, width=4).grid(
            column=2, row=3, sticky=(W, E))

        ttk.Label(self, text="Food Workers").grid(
            column=1, row=4, sticky=(W, E))
        ttk.Label(self, textvariable=self.food_workers, width=4).grid(
            column=2, row=4, sticky=(W, E))

        ttk.Label(self, text="Wood Workers").grid(
            column=1, row=5, sticky=(W, E))
        ttk.Label(self, textvariable=self.wood_workers, width=4).grid(
            column=2, row=5, sticky=(W, E))

        ttk.Label(self, text="Gold Workers").grid(
            column=1, row=6, sticky=(W, E))
        ttk.Label(self, textvariable=self.gold_workers, width=4).grid(
            column=2, row=6, sticky=(W, E))

        ttk.Label(self, text="Stone Workers").grid(
            column=1, row=7, sticky=(W, E))
        ttk.Label(self, textvariable=self.stone_workers,
                  width=4).grid(column=2, row=7, sticky=(W, E))

        ttk.Checkbutton(self, text="Use Static Image", variable=self.debug_static_image_var,
                        command=self.controller.toggle_debug_static_image).grid(
            column=1, row=9, sticky=(W, E))

        # Continuous OCR button
        self.continuous_button_text = StringVar(
            value="Start Scanning")  # Dynamic button text
        ttk.Button(self, textvariable=self.continuous_button_text,
                   command=self.toggle_continuous_ocr).grid(column=3, row=9, sticky=(W, E))

        # Configure padding for all children
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

        # Bind Enter key to perform OCR
        self.master.bind(
            "<Return>", lambda event: self.get_results_from_controller())

        # Start the GUI update loop
        # self.master.after(100, self.update_gui)

    def get_results_from_controller(self):
        try:
            results = self.controller.get_ocr_results()  # Get results from the queue
            if results:
                self.population.set(results['population'])
                self.idle_workers.set(results['idle_worker'])
                self.food_workers.set(results['food_worker'])
                self.wood_workers.set(results['wood_worker'])
                self.gold_workers.set(results['gold_worker'])
                self.stone_workers.set(results['stone_worker'])
        except Exception as e:
            print(f"Error updating GUI: {e}")

    def toggle_continuous_ocr(self):
        """Handle the continuous OCR toggle."""
        if self.controller.is_running:
            # Stop continuous OCR
            self.controller.stop()
            self.continuous_button_text.set("Start Scanning")
        else:
            # Start continuous OCR
            self.controller.start()
            self.continuous_button_text.set("Stop Scanning")

    def start_gui_update_loop(self):
        """Start a loop to periodically update the GUI with OCR results."""
        self.get_results_from_controller()
        self.master.after(500, self.start_gui_update_loop)
