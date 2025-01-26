from tkinter import *
from tkinter import ttk


class SettingsTab(ttk.Frame):
    def __init__(self, parent, settings):
        """
        Initialize the SettingsTab.

        Args:
            parent: The parent widget (usually a notebook or frame).
            settings (Settings): An instance of the Settings class.
        """
        super().__init__(parent)
        self.settings = settings

        # Create variables for each setting
        self.consecutive_readings_var = IntVar(
            value=self.settings.consecutive_readings)
        self.loop_interval_var = DoubleVar(value=self.settings.loop_interval)
        self.tolerance_var = IntVar(value=self.settings.tolerance)
        self.enable_ocr_var = BooleanVar(value=self.settings.enable_ocr)
        self.enable_worker_producing_var = BooleanVar(
            value=self.settings.enable_worker_producing)
        self.debug_static_image_var = BooleanVar(
            value=self.settings.debug_static_image)

        # Bind changes to the settings
        self.consecutive_readings_var.trace_add("write", lambda *args: setattr(
            self.settings, "consecutive_readings", self.consecutive_readings_var.get()))
        self.loop_interval_var.trace_add(
            "write", lambda *args: setattr(self.settings, "loop_interval", self.loop_interval_var.get()))
        self.tolerance_var.trace_add(
            "write", lambda *args: setattr(self.settings, "tolerance", self.tolerance_var.get()))
        self.enable_ocr_var.trace_add(
            "write", lambda *args: setattr(self.settings, "enable_ocr", self.enable_ocr_var.get()))
        self.enable_worker_producing_var.trace_add("write", lambda *args: setattr(
            self.settings, "enable_worker_producing", self.enable_worker_producing_var.get()))
        self.debug_static_image_var.trace_add("write", lambda *args: setattr(
            self.settings, "debug_static_image", self.debug_static_image_var.get()))

        # Set up the UI
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the user interface for the settings tab.
        """
        # Create a frame to hold the settings
        settings_frame = ttk.Frame(self)
        settings_frame.grid(column=0, row=0, sticky=(W, E, N, S))

        # Add padding to all children
        for child in settings_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

        # Consecutive Readings (Slider: 1 to 4, step 1)
        ttk.Label(settings_frame, text="Consecutive Readings:").grid(
            column=0, row=0, sticky=W)
        self.consecutive_readings_slider = ttk.Scale(
            settings_frame,
            from_=1,
            to=4,
            variable=self.consecutive_readings_var,
            orient=HORIZONTAL,
            length=200,
            command=lambda value: self.consecutive_readings_var.set(
                round(float(value)))
        )
        self.consecutive_readings_slider.grid(column=1, row=0, sticky=W)
        self.consecutive_readings_label = ttk.Label(
            settings_frame, text=str(self.consecutive_readings_var.get()))
        self.consecutive_readings_label.grid(column=2, row=0, sticky=W)

        # Loop Interval (Slider: 0.2 to 5.0, step 0.1)
        ttk.Label(settings_frame, text="Loop Interval (seconds):").grid(
            column=0, row=1, sticky=W)
        self.loop_interval_slider = ttk.Scale(
            settings_frame,
            from_=0.2,
            to=5.0,
            variable=self.loop_interval_var,
            orient=HORIZONTAL,
            length=200,
            command=lambda value: self.loop_interval_var.set(
                round(float(value) * 10) / 10)
        )
        self.loop_interval_slider.grid(column=1, row=1, sticky=W)
        self.loop_interval_label = ttk.Label(
            settings_frame, text=f"{self.loop_interval_var.get():.1f}")
        self.loop_interval_label.grid(column=2, row=1, sticky=W)

        # Tolerance (Slider: 0 to 10, step 1)
        ttk.Label(settings_frame, text="Tolerance:").grid(
            column=0, row=2, sticky=W)
        self.tolerance_slider = ttk.Scale(
            settings_frame,
            from_=0,
            to=10,
            variable=self.tolerance_var,
            orient=HORIZONTAL,
            length=200,
            command=lambda value: self.tolerance_var.set(round(float(value)))
        )
        self.tolerance_slider.grid(column=1, row=2, sticky=W)
        self.tolerance_label = ttk.Label(
            settings_frame, text=str(self.tolerance_var.get()))
        self.tolerance_label.grid(column=2, row=2, sticky=W)

        # Enable OCR (Checkbox on the right, centered)
        ttk.Label(settings_frame, text="Enable OCR:").grid(
            column=0, row=3, sticky=W)
        self.enable_ocr_checkbox = ttk.Checkbutton(
            settings_frame, variable=self.enable_ocr_var)
        self.enable_ocr_checkbox.grid(column=1, row=3, sticky="")  # Centered

        # Enable Worker Producing (Checkbox on the right, centered)
        ttk.Label(settings_frame, text="Enable Worker Producing:").grid(
            column=0, row=4, sticky=W)
        self.enable_worker_producing_checkbox = ttk.Checkbutton(
            settings_frame, variable=self.enable_worker_producing_var)
        self.enable_worker_producing_checkbox.grid(
            column=1, row=4, sticky="")  # Centered

        # Debug Static Image (Checkbox on the right, centered)
        ttk.Label(settings_frame, text="Debug Static Image:").grid(
            column=0, row=5, sticky=W)
        self.debug_static_image_checkbox = ttk.Checkbutton(
            settings_frame, variable=self.debug_static_image_var)
        self.debug_static_image_checkbox.grid(
            column=1, row=5, sticky="")  # Centered

        # Reset to Defaults button
        reset_button = ttk.Button(
            settings_frame, text="Reset to Defaults", command=self.reset_to_defaults)
        reset_button.grid(column=0, row=6, columnspan=3, pady=10)

        # Update labels when sliders change
        self.consecutive_readings_var.trace_add(
            "write", self._update_consecutive_readings_label)
        self.loop_interval_var.trace_add(
            "write", self._update_loop_interval_label)
        self.tolerance_var.trace_add("write", self._update_tolerance_label)

    def _update_consecutive_readings_label(self, *args):
        """Update the consecutive readings label."""
        self.consecutive_readings_label.config(
            text=str(self.consecutive_readings_var.get()))

    def _update_loop_interval_label(self, *args):
        """Update the loop interval label."""
        self.loop_interval_label.config(
            text=f"{self.loop_interval_var.get():.1f}")

    def _update_tolerance_label(self, *args):
        """Update the tolerance label."""
        self.tolerance_label.config(text=str(self.tolerance_var.get()))

    def reset_to_defaults(self):
        """Reset all settings to their default values."""
        default_settings = {
            "consecutive_readings": 2,
            "loop_interval": 1.0,
            "tolerance": 0,
            "enable_ocr": True,
            "enable_worker_producing": True,
            "debug_static_image": False,
        }

        # Update the settings
        for key, value in default_settings.items():
            setattr(self.settings, key, value)

        # Update the UI
        self.consecutive_readings_var.set(
            default_settings["consecutive_readings"])
        self.loop_interval_var.set(default_settings["loop_interval"])
        self.tolerance_var.set(default_settings["tolerance"])
        self.enable_ocr_var.set(default_settings["enable_ocr"])
        self.enable_worker_producing_var.set(
            default_settings["enable_worker_producing"])
        self.debug_static_image_var.set(default_settings["debug_static_image"])
