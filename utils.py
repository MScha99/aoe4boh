from tkinter import PhotoImage
import json
import os
from data import civs


def load_emoticons():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Resolve the path to emoticons.json
    emoticon_file_path = os.path.join(script_dir, "assets", "emoticons.json")

    try:
        # Open the emoticon file in read mode
        with open(emoticon_file_path, "r") as file:
            # Load the JSON data from the file
            emoticons = json.load(file)

        # Iterate over each key-value pair in the emoticons dictionary
        for key, path in emoticons.items():
            try:
                # Resolve the full path of the emoticon image file
                resolved_path = os.path.join(script_dir, "assets", path)
                # print(f"Resolved path: {resolved_path}")  # Debugging: Print the resolved path

                # Load the image file as a PhotoImage object and update the dictionary
                emoticons[key] = PhotoImage(file=resolved_path)
                # print(f"Successfully loaded: {key}")  # Debugging: Confirm successful load
            except Exception as e:
                # print(f"Failed to load {key}: {e}")  # Debugging: Print error if loading fails
                emoticons[key] = None  # Set to None if loading fails

        # Return the updated emoticons dictionary
        return emoticons
    except Exception as e:
        # Debugging: Print error if JSON loading fails
        print(f"Failed to load emoticons: {e}")
        return {}  # Return an empty dictionary if loading fails


def setup_builds_directories(base_dir="build_orders"):
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    for civ in civs:        
        civ_dir = os.path.join(base_dir, civ)
        if not os.path.exists(civ_dir):
            os.makedirs(civ_dir)

