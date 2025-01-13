import cv2
import numpy as np
from data import civ_data, vil_data

# Iterate through each civilization and villager
for civ_name, civ_image in civ_data:
    print("\n")
    for vil_name, vil_image in vil_data:
        

        # Crop the civilization image to the worker area
        haystack_cropped_worker = civ_image[640:780, 0:60]

        # Crop the needle image (remove top-left corner)
        cropped_needle = vil_image[:, 13:]

        # Convert to grayscale
        haystack_gray = cv2.cvtColor(haystack_cropped_worker, cv2.COLOR_BGR2GRAY)
        needle_gray = cv2.cvtColor(cropped_needle, cv2.COLOR_BGR2GRAY)

        # Create a mask for the needle (black out the top-left corner)
        mask = np.ones_like(needle_gray) * 255
        mask[0:20, 0:20] = 0  # Mask the top-left 20x20 region

        # Perform grayscale matching with masking
        result_gray = cv2.matchTemplate(haystack_gray, needle_gray, cv2.TM_CCOEFF_NORMED, mask=mask)
        min_val_gray, max_val_gray, min_loc_gray, max_loc_gray = cv2.minMaxLoc(result_gray)


        # Get the dimensions of the cropped needle
        needle_height, needle_width = cropped_needle.shape[:2]

        # Draw a rectangle around the matched region in the haystack image
        top_left = max_loc_gray  # Top-left corner of the matched region
        bottom_right = (top_left[0] + needle_width, top_left[1] + needle_height)  # Bottom-right corner
        cv2.rectangle(haystack_cropped_worker, top_left, bottom_right, (0, 0, 255), 2)  # Red rectangle

        # Display the result
        # print(f"Grayscale Matching Confidence: {max_val_gray:.2f}")
        # print(f"ORB Feature Matching Average Distance: {avg_distance:.2f}")
        # print(f"Combined Confidence: {combined_confidence:.2f} \n")

        if max_val_gray > 0.85:  # Adjust threshold as needed
            print(f"Civilization: {civ_name}")
            print(f"Checking Villager: {vil_name}")
            print(f"Grayscale Matching Confidence: {max_val_gray:.2f}")
           
            cv2.imshow('Matched Result', haystack_cropped_worker)
            cv2.waitKey(0)
            cv2.destroyAllWindows()