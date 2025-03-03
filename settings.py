import json
import os


class Settings:
    def __init__(self, filename="settings.json"):
        """
        Initialize the Settings class.

        Args:
            filename (str): The name of the file where settings are stored. Defaults to "settings.json".
        """
        super().__setattr__("filename", filename)
        super().__setattr__("settings", self._load_settings())

    def _load_settings(self):
        """
        Load settings from the file. If the file doesn't exist, create it with default values.

        Returns:
            dict: The loaded settings.
        """
        default_settings = {
            "consecutive_readings": 2,
            "loop_interval": 1.0,
            "tolerance": 0,
            "enable_ocr": True,
            "enable_worker_producing": True,
            "debug_static_image": False,
            "active_build_order": None

        }

        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as file:
                    return json.load(file)
            except (json.JSONDecodeError, IOError):
                print(f"Error loading settings from {
                      self.filename}. Using default settings.")
                return default_settings
        else:
            # Create the file with default settings
            with open(self.filename, "w") as file:
                json.dump(default_settings, file, indent=4)
            return default_settings
            
    def save_settings(self):
        try:
            with open(self.filename, "w") as file:
                json.dump(self.settings, file, indent=4)
        except IOError:
            print(f"Error saving settings to {self.filename}.")

    def __getattr__(self, name):
        if name in self.settings:
            return self.settings[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        # Prevent modification of special attributes
        if name in ["filename", "settings"]:
            raise AttributeError(f"Cannot modify attribute '{name}' after initialization.")

        # Only allow modification of existing settings
        if name not in self.settings:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'. Cannot create new settings.")

        # Update the setting and save
        self.settings[name] = value
        self.save_settings()