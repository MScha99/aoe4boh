import cv2
import pytesseract
import numpy as np
from data import worker_location_on_screen
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict, deque
import threading

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'./tesseract/tesseract.exe'


def preprocess_image(cropped_image, scale=2, grayscale=True, contrast=2.0,
                     sharpen=False, invert=False, threshold=False, debug=False):
    """
    Preprocesses an image for OCR by applying a series of transformations.

    Args:
        cropped_image (numpy.ndarray): The input image to preprocess.
        scale (float): Scaling factor to resize the image. Default is 2.
        grayscale (bool): Whether to convert the image to grayscale. Default is True.
        contrast (float): Factor to adjust the contrast of the image. Default is 2.0.
        sharpen (bool): Whether to apply a sharpening filter to the image. Default is False.
        invert (bool): Whether to invert the colors of the image. Default is False.
        threshold (bool): Whether to apply binary thresholding to the image. Default is False.
        debug (bool): Whether to display intermediate images for debugging. Default is False.

    Returns:
        numpy.ndarray: The preprocessed image.

    Raises:
        ValueError: If the input image is invalid or preprocessing parameters are out of range.
    """
    # Validate input
    if cropped_image is None or cropped_image.size == 0:
        raise ValueError("Input image is None or invalid.")
    if scale <= 0:
        raise ValueError("Scale factor must be a positive number.")
    if contrast < 0:
        raise ValueError("Contrast value must be non-negative.")

    # Scale the image to improve OCR accuracy
    preprocessed_image = cv2.resize(
        cropped_image, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)

    # Convert the image to grayscale if required
    if grayscale:
        preprocessed_image = cv2.cvtColor(
            preprocessed_image, cv2.COLOR_BGR2GRAY)

    # Adjust the contrast of the image
    if contrast != 1.0:
        alpha = contrast  # Contrast control (1.0 means no change)
        beta = 0  # Brightness control (0 means no change)
        preprocessed_image = cv2.convertScaleAbs(
            preprocessed_image, alpha=alpha, beta=beta)

    # Apply a sharpening filter to enhance edges
    if sharpen:
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        preprocessed_image = cv2.filter2D(preprocessed_image, -1, kernel)

    # Invert the colors of the image (useful for dark text on light backgrounds)
    if invert:
        preprocessed_image = cv2.bitwise_not(preprocessed_image)

    # Apply binary thresholding to create a black-and-white image
    if threshold:
        _, preprocessed_image = cv2.threshold(
            preprocessed_image, 128, 255, cv2.THRESH_BINARY)

    # Display intermediate images for debugging purposes
    if debug:
        cv2.imshow('Original Image', cropped_image)
        cv2.waitKey(0)
        cv2.imshow('Preprocessed Image', preprocessed_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return preprocessed_image


class OCRProcessor:
    def __init__(self, consecutive_readings=3):
        """
        Initialize the OCR processor.

        Args:
            consecutive_readings (int): Number of consecutive consistent readings required
                                       to consider a result valid. Default is 3.
        """
        self.consecutive_readings = consecutive_readings
        # A buffer to store the last N readings for each region
        self.readings_buffer = defaultdict(lambda: deque(maxlen=consecutive_readings))
        # A dictionary to store the last valid result for each region
        self.last_valid_results = {}
        # A lock to ensure thread-safe access to shared resources
        self.lock = threading.Lock()

    def crop_and_ocr(self, ingame_screenshot, worker_location_on_screen=worker_location_on_screen, debug=False):
        """
        Perform OCR on cropped regions of the screenshot.

        This method crops specific regions from the screenshot, preprocesses them,
        and performs OCR to extract text. It uses a ThreadPoolExecutor to process
        regions in parallel for improved performance.

        Args:
            ingame_screenshot (numpy.ndarray): The input screenshot.
            worker_location_on_screen (dict): A dictionary defining the regions to process.
                                              Each region is specified as a percentage of
                                              the screenshot dimensions.
            debug (bool): Whether to display debug images and print intermediate results.

        Returns:
            dict: A dictionary containing the OCR results for each region.
        """
        results = {}

        # Create a copy of the screenshot for debugging purposes
        if debug:
            debug_image = ingame_screenshot.copy()

        def process_region(region_name, region):
            """
            Process a single region: crop, preprocess, and perform OCR.

            Args:
                region_name (str): The name of the region (e.g., "population").
                region (dict): A dictionary containing the region's coordinates as percentages.

            Returns:
                tuple: A tuple containing the region name and the extracted text.
            """
            # Calculate pixel coordinates from percentages
            x = int(region["x"] * ingame_screenshot.shape[1] / 100)
            y = int(region["y"] * ingame_screenshot.shape[0] / 100)
            width = int(region["width"] * ingame_screenshot.shape[1] / 100)
            height = int(region["height"] * ingame_screenshot.shape[0] / 100)

            # Crop the region from the screenshot
            cropped_image = ingame_screenshot[y:y+height, x:x+width]

            # Check if the cropped image is valid
            if cropped_image is None or cropped_image.size == 0:
                print(f"Warning: Cropped image for region '{
                      region_name}' is empty. Skipping.")
                return region_name, ""

            # Preprocess the image to improve OCR accuracy
            preprocessed_image = preprocess_image(cropped_image)

            # Perform OCR on the cropped, preprocessed image
            text = pytesseract.image_to_string(
                preprocessed_image,
                config='-c tessedit_char_whitelist=0123456789/ --psm 7 --oem 1'
            ).strip()

            # Add debug information to the debug image
            if debug:
                # Draw the region bounding box
                cv2.rectangle(debug_image, (x, y),
                              (x + width, y + height), (0, 255, 0), 2)
                # Add OCR text as a label
                cv2.putText(debug_image, text, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            return region_name, text

        # Use ThreadPoolExecutor to process regions in parallel
        with ThreadPoolExecutor() as executor:
            # Submit tasks for each region to the executor
            futures = [executor.submit(process_region, region_name, region)
                       for region_name, region in worker_location_on_screen.items()]
            # Collect results from the futures
            for future in futures:
                region_name, text = future.result()
                with self.lock:
                    # Add the result to the readings buffer
                    self.readings_buffer[region_name].append(text)

                    if debug:
                        print(f"Buffer for {region_name}: {
                          self.readings_buffer[region_name]}")

                    # If the buffer is not fully filled, return the most recent reading
                    if len(self.readings_buffer[region_name]) < self.consecutive_readings:
                        results[region_name] = text
                    else:
                        # Check if the last N readings are the same
                        if len(set(self.readings_buffer[region_name])) == 1:
                            # Update the result and store it as the last valid result
                            results[region_name] = text
                            self.last_valid_results[region_name] = text
                        else:
                            # If readings are inconsistent, use the last valid result
                            results[region_name] = self.last_valid_results.get(
                                region_name, "")

        # Display the debug image if debug mode is enabled
        if debug:
            cv2.imshow("Debug: OCR Regions", debug_image[600:, 0:600])
            cv2.waitKey(0)  # Wait for a key press to close the debug window
            cv2.destroyAllWindows()
            print("Results:", results)
            print("Readings Buffer:", self.readings_buffer)
            print("Last Valid Results:", self.last_valid_results)

        return results