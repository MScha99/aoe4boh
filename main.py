import cv2
import numpy as np
import pytesseract
from screeninfo import get_monitors

from screencap import capture_window
import time  # Import the time module
from tkinter import *
from tkinter import ttk
# from gui import TestGUI
from gui import MainWindow
from villager_locator import VillagerLocator
from settings import Settings
from controller import Controller
from utils import load_emoticons

# monitors = get_monitors()


# villagerlocator=VillagerLocator()

# villagerlocator.find_villager_portrait(capture_window())

# print(villagerlocator.find_villager_portrait(cv2.imread("crop_jap.png")))
settings=Settings()
controller=Controller(settings)
root = Tk()
emoticons = load_emoticons()
main_window=MainWindow(root, settings, controller, emoticons)
root.mainloop()