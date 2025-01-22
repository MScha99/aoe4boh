# gui/ocr_tab.py
from tkinter import *
from tkinter import ttk
import cv2
import threading
import queue
from ocr import OCRProcessor
from screencap import capture_window

class OcrTab(ttk.Frame):
    def __init__(self, parent, consecutive_readings=3):
        super().__init__(parent)
        self.ocr_processor = OCRProcessor(consecutive_readings)
        self.is_running_continuous = False  # Track continuous OCR state
        self.ocr_queue = queue.Queue()  # Queue for thread-safe communication
        self.setup_ui()

    def setup_ui(self):
        # Define StringVars for each label
        self.population = StringVar()
        self.idle_workers = StringVar()
        self.food_workers = StringVar()
        self.wood_workers = StringVar()
        self.gold_workers = StringVar()
        self.stone_workers = StringVar()

        # Toggle states
        self.use_static_image = BooleanVar(value=False)  # Default to static image

        # Create labels and associate them with StringVars
        ttk.Label(self, text="Populacja").grid(column=1, row=2, sticky=(W, E))
        ttk.Label(self, textvariable=self.population).grid(column=2, row=2, sticky=(W, E))

        ttk.Label(self, text="Idle Workers").grid(column=1, row=3, sticky=(W, E))
        ttk.Label(self, textvariable=self.idle_workers, width=4).grid(column=2, row=3, sticky=(W, E))

        ttk.Label(self, text="Food Workers").grid(column=1, row=4, sticky=(W, E))
        ttk.Label(self, textvariable=self.food_workers, width=4).grid(column=2, row=4, sticky=(W, E))

        ttk.Label(self, text="Wood Workers").grid(column=1, row=5, sticky=(W, E))
        ttk.Label(self, textvariable=self.wood_workers, width=4).grid(column=2, row=5, sticky=(W, E))

        ttk.Label(self, text="Gold Workers").grid(column=1, row=6, sticky=(W, E))
        ttk.Label(self, textvariable=self.gold_workers, width=4).grid(column=2, row=6, sticky=(W, E))

        ttk.Label(self, text="Stone Workers").grid(column=1, row=7, sticky=(W, E))
        ttk.Label(self, textvariable=self.stone_workers, width=4).grid(column=2, row=7, sticky=(W, E))

        # Buttons
        ttk.Button(self, text="Scan once", command=self.perform_ocr).grid(column=3, row=8, sticky=(W, E))
        ttk.Checkbutton(self, text="Use Static Image", variable=self.use_static_image).grid(column=1, row=9, sticky=(W, E))

        # Continuous OCR button
        self.continuous_button_text = StringVar(value="Start Scanning")  # Dynamic button text
        ttk.Button(self, textvariable=self.continuous_button_text,
                   command=self.toggle_continuous_ocr).grid(column=3, row=9, sticky=(W, E))

        # Configure padding for all children
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

        # Bind Enter key to perform OCR
        self.master.bind("<Return>", self.perform_ocr)

        # Start the GUI update loop
        self.master.after(100, self.update_gui)

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
                self.master.after(1000, self.perform_ocr)  # Schedule next execution after 1 second

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
            self.master.after(100, self.update_gui)  # Schedule the next GUI update

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