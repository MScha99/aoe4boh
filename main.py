import cv2
import numpy as np
import pytesseract
from screeninfo import get_monitors
from ocr import ocr_onto_cropped_areas
from screencap import capture_window
import time  # Import the time module
from tkinter import *
from tkinter import ttk
from gui import test_gui

monitors = get_monitors()


# start_time_capture = time.perf_counter()  # Start timing
# for i in range(20):
#     print(ocr_onto_cropped_areas(capture_window()))
# end_time_capture = time.perf_counter()  # End timing
# elapsed_time_capture = end_time_capture - start_time_capture  # Calculate elapsed time
# print(f"Time taken for capture-based loop: {elapsed_time_capture:.4f} seconds")


# print(ocr_onto_cropped_areas(capture_window(), debug=True))
# print(ocr_onto_cropped_areas(cv2.imread('jap.png'), debug=True))

# results = (ocr_onto_cropped_areas(cv2.imread('jap.png'), debug=False))
# print(results['population'])
 
root = Tk()
test_gui(root)
root.mainloop()