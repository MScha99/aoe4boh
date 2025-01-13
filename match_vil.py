import cv2
import numpy as np
from data import vil_data

def match_vil(ingame_screenshot):
    # Iterate through each villager needle image to find the matching one
    curr_best_match = 0
    matched_vil = ''
    for vil_name, vil_image in vil_data:

        # Crop the ingame image to the worker area
        haystack_cropped_worker = ingame_screenshot[640:780, 0:60]

        # Crop the needle image (remove top-left corner)
        # cropped_needle = vil_image[:, 13:]

        # Convert to grayscale
        haystack_gray = cv2.cvtColor(
            haystack_cropped_worker, cv2.COLOR_BGR2GRAY)
        needle_gray = cv2.cvtColor(vil_image, cv2.COLOR_BGR2GRAY)

        # Mask the top-left region where dynamic vil queue is displayed
        mask = np.ones_like(needle_gray) * 255
        mask[0:14, 0:14] = 0

        # Perform grayscale matching with masking
        result_gray = cv2.matchTemplate(
            haystack_gray, needle_gray, cv2.TM_CCOEFF_NORMED, mask=mask)
        min_val_gray, max_val_gray, min_loc_gray, max_loc_gray = cv2.minMaxLoc(
            result_gray)

        # Update the best match if a better one is found
        if max_val_gray > curr_best_match:
            curr_best_match = max_val_gray
            matched_vil = vil_name

        ###################################### debuging ############################################
        # # Get the dimensions of the cropped needle
        # needle_height, needle_width = vil_image.shape[:2]

        # # Draw a rectangle around the matched region in the haystack image
        # top_left = max_loc_gray
        # bottom_right = (top_left[0] + needle_width,
        #                 top_left[1] + needle_height)
        # cv2.rectangle(haystack_cropped_worker, top_left,
        #               bottom_right, (0, 0, 255), 2)  # Red

        # # only show high confidence results
        # if max_val_gray > 0.85:
        #     print(f"Checking Villager: {vil_name}")
        #     print(f"Grayscale Matching Confidence: {max_val_gray:.2f}")

        #     cv2.imshow('Matched Result', haystack_cropped_worker)
        #     cv2.waitKey(0)
        #     cv2.destroyAllWindows()
        ###################################### debuging ############################################

    return matched_vil
