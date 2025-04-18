import cv2
import numpy as np
from ctypes import windll
import win32gui
import win32ui


def capture_window(window_title="Age of Empires IV "):
    # Ensure the process is DPI-aware
    windll.user32.SetProcessDPIAware()

    # Find the window handle by its title
    hwnd = win32gui.FindWindow(None, window_title)
    if not hwnd:
        raise Exception(f"Window '{window_title}' not found!")

    # Get the client area dimensions
    left, top, right, bottom = win32gui.GetClientRect(hwnd)
    width = right - left
    height = bottom - top

    # Get the window's device context (DC)
    hwnd_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    save_dc = mfc_dc.CreateCompatibleDC()

    # Create a bitmap to save the screenshot
    bitmap = win32ui.CreateBitmap()
    bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
    save_dc.SelectObject(bitmap)

    # Use PrintWindow to capture the window's content
    result = windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 3)

    # Convert the bitmap to a NumPy array
    bmp_info = bitmap.GetInfo()
    bmp_str = bitmap.GetBitmapBits(True)
    img = np.frombuffer(bmp_str, dtype=np.uint8).reshape(
        (bmp_info["bmHeight"], bmp_info["bmWidth"], 4))

    # Drop the alpha channel and make the image contiguous
    img = np.ascontiguousarray(img[..., :3])  # Keep only RGB channels

    # Clean up
    win32gui.DeleteObject(bitmap.GetHandle())
    save_dc.DeleteDC()
    mfc_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwnd_dc)

    if not result:  # If PrintWindow failed
        raise RuntimeError(f"Unable to acquire screenshot! Result: {result}")

    return img
