# gui/ocr_tab.py
from tkinter import *
from tkinter import ttk


class OcrTab(ttk.Frame):
    def __init__(self, parent, settings, controller):
        super().__init__(parent)
        self.settings = settings
        self.controller = controller

        # import settings into BooleanVar that are tied to checkboxes to easy tracking of changes
        self.enable_ocr = BooleanVar(value=self.settings.enable_ocr)
        self.enable_worker_producing = BooleanVar(
            value=self.settings.enable_worker_producing)
        self.debug_static_image_var = BooleanVar(
            value=self.settings.debug_static_image)

        # when the value of the variable changes, update the settings
        self.enable_ocr.trace_add(
            "write", lambda *args: setattr(self.settings, "enable_ocr", self.enable_ocr.get()))
        self.enable_worker_producing.trace_add("write", lambda *args: setattr(
            self.settings, "enable_worker_producing", self.enable_worker_producing.get()))
        self.debug_static_image_var.trace_add("write", lambda *args: setattr(
            self.settings, "debug_static_image", self.debug_static_image_var.get()))

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
        self.worker_producing = StringVar()

        # Create labels and associate them with StringVars
        ttk.Checkbutton(self, text="Enable OCR", variable=self.enable_ocr,
                        onvalue=True, offvalue=False).grid(column=1, row=0, sticky=(W, E))

        ttk.Checkbutton(self, text="Enable worker checking", variable=self.enable_worker_producing,
                        onvalue=True, offvalue=False).grid(column=1, row=1, sticky=(W, E))

        ttk.Label(self, text="Worker:").grid(
            column=1, row=2, columnspan=2, sticky=(W, E))
        ttk.Label(self, textvariable=self.worker_producing, width=4).grid(
            column=2, row=2, columnspan=2, sticky=(W, E))

        ttk.Label(self, text="Populacja").grid(column=1, row=3, sticky=(W, E))
        ttk.Label(self, textvariable=self.population).grid(
            column=2, row=3, sticky=(W, E))

        ttk.Label(self, text="Idle Workers").grid(
            column=1, row=4, sticky=(W, E))
        ttk.Label(self, textvariable=self.idle_workers, width=4).grid(
            column=2, row=4, sticky=(W, E))

        ttk.Label(self, text="Food Workers").grid(
            column=1, row=5, sticky=(W, E))
        ttk.Label(self, textvariable=self.food_workers, width=4).grid(
            column=2, row=5, sticky=(W, E))

        ttk.Label(self, text="Wood Workers").grid(
            column=1, row=6, sticky=(W, E))
        ttk.Label(self, textvariable=self.wood_workers, width=4).grid(
            column=2, row=6, sticky=(W, E))

        ttk.Label(self, text="Gold Workers").grid(
            column=1, row=7, sticky=(W, E))
        ttk.Label(self, textvariable=self.gold_workers, width=4).grid(
            column=2, row=7, sticky=(W, E))

        ttk.Label(self, text="Stone Workers").grid(
            column=1, row=8, sticky=(W, E))
        ttk.Label(self, textvariable=self.stone_workers,
                  width=4).grid(column=2, row=8, sticky=(W, E))

        ttk.Checkbutton(self, text="Use Static Image", variable=self.debug_static_image_var,).grid(
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
