import threading
import queue
import time
from ocr import OCRProcessor
from screencap import capture_window
import cv2


class Controller:
    def __init__(self, consecutive_readings=3):
        """
        Initialize the Controller.

        Args:
            consecutive_readings (int): Number of consecutive consistent readings required
                                       to consider a result valid. Default is 3.
        """
        self.ocr_processor = OCRProcessor(consecutive_readings)
        self.is_running = False  # Controls whether the main loop is running
        self.ocr_queue = queue.Queue()  # Queue for thread-safe communication of OCR results
        # Time (in seconds) between iterations of the main loop
        self.loop_interval = 1.0
        self.debug_static_image = False

    def toggle_debug_static_image(self):
        """
        This method switches the value of `debug_static_image` between True and False.
        """
        self.debug_static_image = not self.debug_static_image

    def start(self):
        """
        Start the main loop in a separate thread.

        This method sets `is_running` to True and starts a new thread to run the main loop.
        """
        self.is_running = True
        threading.Thread(target=self._run_loop, daemon=True).start()

    def stop(self):
        """
        Stop the main loop.

        This method sets `is_running` to False, signaling the main loop to exit.
        """
        self.is_running = False

    def _run_loop(self):
        """
        Main loop that captures the screenshot and processes it for OCR.

        This loop runs continuously while `is_running` is True. It captures the screenshot,
        starts a new thread for OCR processing, and waits for the next iteration.
        """
        while self.is_running:
            try:

                if self.debug_static_image:
                    image = cv2.imread("macro.png")
                else:
                    # Capture the screenshot
                    image = capture_window()

                # Process the image for OCR in a separate thread
                threading.Thread(target=self._perform_ocr,
                                 args=(image,), daemon=True).start()

            except Exception as e:

                print(f"Error in main loop: {e}")

            # Wait for the next iteration
            time.sleep(self.loop_interval)

    def _perform_ocr(self, image):
        """
        Crop the image, preprocess it, perform OCR, and put results in the queue.

        Args:
            image (numpy.ndarray): The screenshot to process.
        """
        try:
            # Perform OCR on the image
            results = self.ocr_processor.crop_and_ocr(image)
            print(results)
            # Put the results in the queue for the GUI thread to consume
            self.ocr_queue.put(results)
        except Exception as e:
            print(f"Error in OCR thread: {e}")

    def get_ocr_results(self):
        """
        Retrieve OCR results from the queue.

        Returns:
            dict: The OCR results for each region, or None if the queue is empty.
        """
        try:
            return self.ocr_queue.get_nowait()
        except queue.Empty:
            return None
