import cv2
import numpy as np
import pytesseract
from screeninfo import get_monitors
from ocr import ocr_onto_cropped_areas
from screencap import capture_window, crop_to_initial_region
import time  # Import the time module

monitors = get_monitors()

# # # Time the first loop (reading from file)
# start_time_file = time.perf_counter()  # Start timing
# for i in range(20):
#     print(ocr_onto_cropped_areas(crop_to_initial_region(cv2.imread("test5.png"))))
# end_time_file = time.perf_counter()  # End timing
# elapsed_time_file = end_time_file - start_time_file  # Calculate elapsed time

# # Time the second loop (capturing from window)
# start_time_capture = time.perf_counter()  # Start timing
# for i in range(20):
#     print(ocr_onto_cropped_areas(crop_to_initial_region(capture_window())))
# end_time_capture = time.perf_counter()  # End timing
# elapsed_time_capture = end_time_capture - start_time_capture  # Calculate elapsed time

# # Print the results
# print(f"Time taken for file-based loop: {elapsed_time_file:.4f} seconds")
# print(f"Time taken for capture-based loop: {elapsed_time_capture:.4f} seconds")


# cv2.imshow("OCR: ", crop_to_initial_region(capture_window()))
# # cv2.imshow("OCR: ", capture_window())
# cv2.waitKey(30000)  # Wait for 1 ms to refresh the display

print(ocr_onto_cropped_areas(crop_to_initial_region(capture_window()), debug=True))