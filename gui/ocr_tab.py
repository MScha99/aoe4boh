from tkinter import *
from tkinter import ttk


class OcrTab(ttk.Frame):
    def __init__(self, parent, settings, controller):
        """
        Initialize the OcrTab.

        Args:
            parent: The parent widget (usually a notebook or frame).
            settings (Settings): An instance of the Settings class.
            controller (Controller): An instance of the Controller class.
        """
        super().__init__(parent)
        self.settings = settings
        self.controller = controller

        # Set up the UI
        self.setup_ui()
        self.start_gui_update_loop()

    def setup_ui(self):
        """
        Set up the user interface for the OCR tab.
        """
        # Define StringVars for each label
        self.population = StringVar()
        self.idle_workers = StringVar()
        self.food_workers = StringVar()
        self.wood_workers = StringVar()
        self.gold_workers = StringVar()
        self.stone_workers = StringVar()
        self.worker_producing = StringVar()

        # Configure columns to allocate space properly
        self.columnconfigure(0, weight=1)  # Column 0 (labels) will expand
        self.columnconfigure(1, weight=1)  # Column 1 (values) will expand

        # Create labels and associate them with StringVars
        ttk.Label(self, text="Worker:").grid(column=0, row=0, sticky=W)
        ttk.Label(self, textvariable=self.worker_producing).grid(column=1, row=0, sticky=W)

        ttk.Label(self, text="Populacja:").grid(column=0, row=1, sticky=W)
        ttk.Label(self, textvariable=self.population).grid(column=1, row=1, sticky=W)

        ttk.Label(self, text="Idle Workers:").grid(column=0, row=2, sticky=W)
        ttk.Label(self, textvariable=self.idle_workers).grid(column=1, row=2, sticky=W)

        ttk.Label(self, text="Food Workers:").grid(column=0, row=3, sticky=W)
        ttk.Label(self, textvariable=self.food_workers).grid(column=1, row=3, sticky=W)

        ttk.Label(self, text="Wood Workers:").grid(column=0, row=4, sticky=W)
        ttk.Label(self, textvariable=self.wood_workers).grid(column=1, row=4, sticky=W)

        ttk.Label(self, text="Gold Workers:").grid(column=0, row=5, sticky=W)
        ttk.Label(self, textvariable=self.gold_workers).grid(column=1, row=5, sticky=W)

        ttk.Label(self, text="Stone Workers:").grid(column=0, row=6, sticky=W)
        ttk.Label(self, textvariable=self.stone_workers).grid(column=1, row=6, sticky=W)

        # Continuous OCR button
        self.continuous_button_text = StringVar(value="Start Scanning")  # Dynamic button text
        ttk.Button(self, textvariable=self.continuous_button_text, command=self.toggle_continuous_ocr).grid(column=0, row=7, columnspan=2, sticky=(W, E))

        # Configure padding for all children
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

        # Bind Enter key to perform OCR
        self.master.bind("<Return>", lambda event: self.get_results_from_controller())

    def get_results_from_controller(self):
        """
        Retrieve OCR and villager portrait results from the controller and update the GUI.
        """
        try:
            # Get OCR results from the queue
            results = self.controller.get_ocr_results()
            # Get villager portrait results from the queue
            results2 = self.controller.get_villager_portrait_results()

            # Update OCR results in the GUI
            if results:
                self.population.set(results['population'])
                self.idle_workers.set(results['idle_worker'])
                self.food_workers.set(results['food_worker'])
                self.wood_workers.set(results['wood_worker'])
                self.gold_workers.set(results['gold_worker'])
                self.stone_workers.set(results['stone_worker'])

            # Update worker production status in the GUI
            if results2:
                self.worker_producing.set(results2)

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
        self.master.after(200, self.start_gui_update_loop)