import threading
import queue
import time
from ocr import OCRProcessor
from screencap import capture_window
from villager_locator import VillagerLocator
import cv2


class Controller:
    def __init__(self, settings):
        """
        Initialize the Controller.

        Args:
            enable_ocr (bool): Flag to enable or disable OCR processing.
            enable_worker_producing (bool): Flag to enable or disable worker producing detection.
            consecutive_readings (int): Number of consecutive consistent readings required
                        to consider a result valid. Default is 2.
            tolerance (int): Tolerance level for villager locator. Default is 0.
        """
        self.settings=settings

        self.ocr_processor = OCRProcessor(self.settings.consecutive_readings)
        self.villager_locator = VillagerLocator(self.settings.tolerance)

  
        self.is_running = False  # Controls whether the main loop is running
        self.ocr_queue = queue.Queue()  # Queue for thread-safe communication of OCR results
        # Queue for thread-safe communication of villager location results
        self.villager_queue = queue.Queue()
        # Time (in seconds) between iterations of the main loop



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

                if self.settings.debug_static_image:
                    image = cv2.imread("five.png")
                else:
                    # Capture the screenshot
                    image = capture_window()

                if self.settings.enable_ocr:
                    # Process and perform OCR in a separate thread
                    threading.Thread(target=self._perform_ocr,
                                     args=(image,), daemon=True).start()

                if self.settings.enable_worker_producing:
                    self._perform_search_for_queued_villager(image)

            except Exception as e:

                print(f"Error in main loop: {e}")

            # Wait for the next iteration
            time.sleep(self.settings.loop_interval)

    def _perform_search_for_queued_villager(self, image):
        """
        Perform the search for the villager portrait in the image.

        Args:
            image (numpy.ndarray): The screenshot to process.
        """
        try:
            # Find the villager portrait
            villager_position = self.villager_locator.find_villager_portrait(
                image)
            if villager_position:
                self.villager_queue.put("Villager producing")
                # print(f"Villager found at: {villager_position}")
            else:
                # print("Villager not found.")
                self.villager_queue.put("Make villagers")
        except Exception as e:
            print(f"Error in villager search thread: {e}")

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

    def get_villager_portrait_results(self):
        """
        Retrieve villager portrait results from the queue.

        Returns:
            tuple: The coordinates of the villager portrait, or None if the queue is empty.
        """
        try:
            return self.villager_queue.get_nowait()
        except queue.Empty:
            return None
