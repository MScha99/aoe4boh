from data import villager_distinct_pixels
import numpy as np


class VillagerLocator:
    def __init__(self, tolerance):
        """
        Initialize the VillagerLocator.

        Args:
            tolerance (int): The maximum allowed difference for each color channel.
        """
        self.villager_distinct_pixels = villager_distinct_pixels
        self.tolerance = tolerance

    def _are_colors_similar(self, color1, color2, tolerance):
        """
        Determine if two RGB colors are similar within a given tolerance.

        Args:
            color1 (numpy.ndarray): The first color as a NumPy array of shape (3,).
            color2 (numpy.ndarray): The second color as a NumPy array of shape (3,).
            tolerance (int, optional): The maximum allowed difference for each color component. Defaults to 0.

        Returns:
            bool: True if the colors are similar within the given tolerance, False otherwise.
        """
        # Calculate the absolute difference between the two colors
        diff = np.abs(color1 - color2)
        # Check if all differences are within the tolerance
        return np.all(diff <= tolerance)

    def find_villager_portrait(self, image, crop_area=(11, 655, 47, 769)):
        """
        Scans an image to locate the position of a villager portrait based on a set of distinct pixels.

        Args:
            image (numpy.ndarray): The image in which to search for the villager portrait. Shape: (height, width, 3).
            crop_area (tuple, optional): The crop area as (min_x, min_y, max_x, max_y). Defaults to (11, 655, 11, 733).

        Returns:
            tuple: The (x, y) coordinates of the top-left corner of the matched villager portrait if found.
            None: If no match is found.
        """
        # Crop the image if crop_area is provided
        if crop_area:
            min_x, min_y, max_x, max_y = crop_area
            image = image[min_y:max_y, min_x:max_x]

        else:
            min_x, min_y = 0, 0  # No cropping, so the coordinates are relative to the original image

        height, width, _ = image.shape  # Get image dimensions

        # The first pixel is the reference point
        reference_pixel = self.villager_distinct_pixels[0]
        ref_x, ref_y, ref_color = reference_pixel

        # Ensure ref_color is a NumPy array
        ref_color = np.array(ref_color)

        # Scan the entire image for the reference pixel
        for x in range(width):
            for y in range(height):
                # Get the pixel color at (x, y)
                # NumPy arrays are accessed as (row, column)
                pixel_color = image[y, x]

                # Check if the pixel color matches the reference color
                if self._are_colors_similar(pixel_color, ref_color, self.tolerance):
                    # Reference pixel found! Check the other pixels at their relative positions
                    match = True
                    for rel_x, rel_y, expected_color in self.villager_distinct_pixels[1:]:
                        target_x = x + rel_x
                        target_y = y + rel_y

                        # Avoid out-of-bounds
                        if target_x >= width or target_y >= height:
                            match = False
                            break

                        # Get the pixel color at the target position
                        target_color = image[target_y, target_x]

                        # Ensure expected_color is a NumPy array
                        expected_color = np.array(expected_color)

                        # Check if the target color matches the expected color
                        if not self._are_colors_similar(target_color, expected_color, self.tolerance):
                            match = False
                            break

                    # If all pixels match, return the position (adjusted for cropping)
                    if match:
                        return (x + min_x, y + min_y)

        # If no match is found after scanning the entire image, return None
        return None
