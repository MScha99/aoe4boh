from tkinter import *
from tkinter import ttk
import os
import sys
from ocr import ocr_onto_cropped_areas
import cv2


class test_gui:

    def __init__(self, root):

        root.title("ocr")
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.population = StringVar()
        self.idle_workers = StringVar()
        self.food_workers = StringVar()
        self.wood_workers = StringVar()
        self.gold_workers = StringVar()
        self.stone_workers = StringVar()
        

        ttk.Label(mainframe, text="Populacja").grid(
            column=1, row=2, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.resources['population']).grid(
            column=2, row=2, sticky=(W, E))
        ttk.Button(mainframe, text="perform ocr", command=self.perform_ocr).grid(
            column=3, row=3, sticky=(W, E))
        ttk.Button(root, text="Restart", command=self.restart).grid(
            column=3, row=4, sticky=(W, E))

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        root.bind("<Return>", self.perform_ocr)

    def perform_ocr(self, *args):
        try:
            results=ocr_onto_cropped_areas(cv2.imread("jap.png"))             
            self.resources.set(results)
        except ValueError:
            pass

    def restart(self):
        """Restart the application."""
        python = sys.executable
        os.execl(python, python, *sys.argv)
