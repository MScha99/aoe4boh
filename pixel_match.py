from PIL import Image, ImageDraw
import time

# Define the target pixels: (relative_x, relative_y, expected_color)
# The first pixel is the reference point (relative_x = 0, relative_y = 0)
target_pixels = [
    (0, 0, (22, 25, 38, 255)),    # Reference point (top-left)
    (20, 1, (47, 61, 81, 255)),   # Relative to reference point
    (27, 3, (34, 43, 59, 255)),   # Relative to reference point
    (35, 31, (21, 24, 36, 255)),  # Relative to reference point
]

# Function to check if two colors are similar
def colors_are_similar(color1, color2, tolerance=0):
    r1, g1, b1, a1 = color1
    r2, g2, b2, a2 = color2
    return (abs(r1 - r2) <= tolerance and
            abs(g1 - g2) <= tolerance and
            abs(b1 - b2) <= tolerance and
            abs(a1 - a2) <= tolerance)

# Function to find the portrait in the screenshot and visualize the matches
def find_portrait(screenshot, target_pixels, tolerance=0):
    start_time = time.time()  # Start the timer

    width, height = screenshot.size
    reference_pixel = target_pixels[0]  # The first pixel is the reference point
    ref_x, ref_y, ref_color = reference_pixel

    # Create a copy of the screenshot for visualization
    debug_image = screenshot.copy()
    draw = ImageDraw.Draw(debug_image)

    # Scan the entire screenshot for the reference pixel
    for x in range(width):
        for y in range(height):
            pixel_color = screenshot.getpixel((x, y))
            if colors_are_similar(pixel_color, ref_color, tolerance):
                # Reference pixel found! Check the other pixels at their relative positions
                match = True
                for rel_x, rel_y, expected_color in target_pixels[1:]:
                    target_x = x + rel_x
                    target_y = y + rel_y
                    if (target_x >= width or target_y >= height):  # Avoid out-of-bounds
                        match = False
                        break
                    target_color = screenshot.getpixel((target_x, target_y))
                    if not colors_are_similar(target_color, expected_color, tolerance):
                        match = False
                        break

                # If all pixels match, highlight the matched pixels and return the position
                if match:
                    # Highlight the reference pixel
                    draw.rectangle([x - 1, y - 1, x + 1, y + 1], outline="red", fill="red")
                    # Highlight the other matched pixels
                    for rel_x, rel_y, _ in target_pixels[1:]:
                        target_x = x + rel_x
                        target_y = y + rel_y
                        draw.rectangle([target_x - 1, target_y - 1, target_x + 1, target_y + 1], outline="red", fill="red")

                    end_time = time.time()  # Stop the timer
                    debug_image.show()  # Show the debug image
                    return (x, y), end_time - start_time

    # If no match is found, return None and time taken
    end_time = time.time()
    debug_image.show()  # Show the debug image (no highlights if no match)
    return None, end_time - start_time

# Load the in-game screenshot using PIL
screenshot_path = "crop_jap.png"
screenshot = Image.open(screenshot_path).convert("RGBA")  # Ensure the image is in RGBA mode

# Find the portrait and measure the time taken
position, time_taken = find_portrait(screenshot, target_pixels, tolerance=10)

# Print the results
if position:
    print(f"Portrait found at position: {position}")
else:
    print("Portrait not found.")
print(f"Time taken: {time_taken:.4f} seconds")