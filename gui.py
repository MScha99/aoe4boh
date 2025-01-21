from tkinter import *
from tkinter import ttk
import os
import sys
from ocr import ocr_onto_cropped_areas
from screencap import capture_window
import cv2


class TestGUI:

    def __init__(self, root):
        self.root = root  # Store the root object as an instance variable
        self.root.title("OCR")
        mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Define StringVars for each label
        self.population = StringVar()
        self.idle_workers = StringVar()
        self.food_workers = StringVar()
        self.wood_workers = StringVar()
        self.gold_workers = StringVar()
        self.stone_workers = StringVar()

        # Toggle states
        self.use_static_image = BooleanVar(
            value=True)  # Default to static image
        self.is_running_continuous = False  # Track continuous OCR state

        # Create labels and associate them with StringVars
        ttk.Label(mainframe, text="Populacja").grid(
            column=1, row=2, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.population).grid(
            column=2, row=2, sticky=(W, E))

        ttk.Label(mainframe, text="Idle Workers").grid(
            column=1, row=3, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.idle_workers).grid(
            column=2, row=3, sticky=(W, E))

        ttk.Label(mainframe, text="Food Workers").grid(
            column=1, row=4, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.food_workers).grid(
            column=2, row=4, sticky=(W, E))

        ttk.Label(mainframe, text="Wood Workers").grid(
            column=1, row=5, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.wood_workers).grid(
            column=2, row=5, sticky=(W, E))

        ttk.Label(mainframe, text="Gold Workers").grid(
            column=1, row=6, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.gold_workers).grid(
            column=2, row=6, sticky=(W, E))

        ttk.Label(mainframe, text="Stone Workers").grid(
            column=1, row=7, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.stone_workers).grid(
            column=2, row=7, sticky=(W, E))

        # Static image toggle

        # Buttons
        ttk.Button(mainframe, text="Scan once", command=self.perform_ocr).grid(
            column=3, row=8, sticky=(W, E))
        ttk.Button(self.root, text="Restart", command=self.restart).grid(
            column=3, row=9, sticky=(W, E))
        ttk.Checkbutton(mainframe, text="Use Static Image", variable=self.use_static_image).grid(
            column=1, row=9, sticky=(W, E))

        # Continuous OCR button
        self.continuous_button_text = StringVar(
            value="Start Scanning")  # Dynamic button text
        ttk.Button(mainframe, textvariable=self.continuous_button_text,
                   command=self.toggle_continuous_ocr).grid(column=3, row=9, sticky=(W, E))

        # Configure padding for all children
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        # Bind Enter key to perform OCR
        self.root.bind("<Return>", self.perform_ocr)

    def perform_ocr(self, *args):
        """Perform OCR and update the GUI with results."""
        try:
            # Determine the input source based on the toggle state
            if self.use_static_image.get():
                # Use static image
                image = cv2.imread("jap.png")
            else:
                # Use dynamically captured image
                image = capture_window()

            # Call the OCR function and get the results as a dictionary
            results = ocr_onto_cropped_areas(image)

            # Update StringVars using the set() method
            self.population.set(results['population'])
            self.idle_workers.set(results['idle_worker'])
            self.food_workers.set(results['food_worker'])
            self.wood_workers.set(results['wood_worker'])
            self.gold_workers.set(results['gold_worker'])
            self.stone_workers.set(results['stone_worker'])

            # If continuous OCR is enabled, schedule the next execution
            if self.is_running_continuous:
                # Schedule next execution after 1 second
                self.root.after(1000, self.perform_ocr)

        except Exception as e:
            print(f"Error during OCR: {e}")

    def toggle_continuous_ocr(self):
        """Handle the continuous OCR toggle."""
        if self.is_running_continuous:
            # Stop continuous OCR
            self.is_running_continuous = False
            self.continuous_button_text.set("Start Scanning")
        else:
            # Start continuous OCR
            self.is_running_continuous = True
            self.continuous_button_text.set("Stop Scanning")
            self.perform_ocr()

    def restart(self):
        """Restart the application."""
        python = sys.executable
        os.execl(python, python, *sys.argv)

######
