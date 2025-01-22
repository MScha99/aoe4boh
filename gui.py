from tkinter import *
from tkinter import ttk
import os
import sys
from ocr import OCRProcessor
from screencap import capture_window
import cv2
import threading
import queue


class TestGUI:

    def __init__(self, root, consecutive_readings=3):
        self.root = root  # Store the root object as an instance variable
        self.root.title("OCR")
        mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.ocr_processor = OCRProcessor(consecutive_readings)

        # Define StringVars for each label
        self.population = StringVar()
        self.idle_workers = StringVar()
        self.food_workers = StringVar()
        self.wood_workers = StringVar()
        self.gold_workers = StringVar()
        self.stone_workers = StringVar()

        # Toggle states
        self.use_static_image = BooleanVar(value=False)  # Default to static image
        self.is_running_continuous = False  # Track continuous OCR state

        # Queue for thread-safe communication
        self.ocr_queue = queue.Queue()

        # Create labels and associate them with StringVars
        ttk.Label(mainframe, text="Populacja").grid(column=1, row=2, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.population).grid(column=2, row=2, sticky=(W, E))

        ttk.Label(mainframe, text="Idle Workers").grid(column=1, row=3, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.idle_workers).grid(column=2, row=3, sticky=(W, E))

        ttk.Label(mainframe, text="Food Workers").grid(column=1, row=4, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.food_workers).grid(column=2, row=4, sticky=(W, E))

        ttk.Label(mainframe, text="Wood Workers").grid(column=1, row=5, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.wood_workers).grid(column=2, row=5, sticky=(W, E))

        ttk.Label(mainframe, text="Gold Workers").grid(column=1, row=6, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.gold_workers).grid(column=2, row=6, sticky=(W, E))

        ttk.Label(mainframe, text="Stone Workers").grid(column=1, row=7, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.stone_workers).grid(column=2, row=7, sticky=(W, E))

        # Buttons
        ttk.Button(mainframe, text="Scan once", command=self.perform_ocr).grid(column=3, row=8, sticky=(W, E))
        ttk.Button(self.root, text="Restart", command=self.restart).grid(column=3, row=9, sticky=(W, E))
        ttk.Checkbutton(mainframe, text="Use Static Image", variable=self.use_static_image).grid(column=1, row=9, sticky=(W, E))

        # Continuous OCR button
        self.continuous_button_text = StringVar(value="Start Scanning")  # Dynamic button text
        ttk.Button(mainframe, textvariable=self.continuous_button_text,
                   command=self.toggle_continuous_ocr).grid(column=3, row=9, sticky=(W, E))

        # Configure padding for all children
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        # Bind Enter key to perform OCR
        self.root.bind("<Return>", self.perform_ocr)

        # Start the GUI update loop
        self.root.after(100, self.update_gui)

    def perform_ocr(self, *args):
        """Perform OCR in a separate thread."""
        try:
            # Determine the input source based on the toggle state
            if self.use_static_image.get():
                image = cv2.imread("jap.png")
            else:
                image = capture_window()

            # Start OCR in a separate thread
            threading.Thread(target=self._run_ocr, args=(image,), daemon=True).start()

            # If continuous OCR is enabled, schedule the next execution
            if self.is_running_continuous:
                self.root.after(1000, self.perform_ocr)  # Schedule next execution after 1 second

        except Exception as e:
            print(f"Error during OCR: {e}")

    def _run_ocr(self, image):
        """Run OCR processing in a separate thread."""
        try:
            results = self.ocr_processor.ocr_onto_cropped_areas(image)
            self.ocr_queue.put(results)  # Put results in the queue for GUI updates
        except Exception as e:
            print(f"Error in OCR thread: {e}")

    def update_gui(self):
        """Update the GUI with OCR results from the queue."""
        try:
            while True:
                results = self.ocr_queue.get_nowait()  # Get results from the queue
                self.population.set(results['population'])
                self.idle_workers.set(results['idle_worker'])
                self.food_workers.set(results['food_worker'])
                self.wood_workers.set(results['wood_worker'])
                self.gold_workers.set(results['gold_worker'])
                self.stone_workers.set(results['stone_worker'])
        except queue.Empty:
            pass  # No new results in the queue
        finally:
            self.root.after(100, self.update_gui)  # Schedule the next GUI update

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