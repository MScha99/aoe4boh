from PIL import Image
import os
from PIL import ImageDraw

# Load all villager portrait images
image_folder = "assets\\images"  
image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith("vil.png")]

# Check if any images were found
if not image_files:
    print("No images found in the folder.")
    exit()

# List all found images and their dimensions
print("Found images:")
for image_file in image_files:
    try:
        img = Image.open(image_file).convert("RGBA")  # Convert to RGBA
        print(f"- {image_file}: {img.size[0]}x{img.size[1]}, Mode: {img.mode}")
    except Exception as e:
        print(f"- {image_file}: Error loading image - {e}")

# Load the first image to get dimensions
first_image = Image.open(image_files[0]).convert("RGBA")  # Convert to RGBA
width, height = first_image.size
print(f"\nFirst image dimensions: {width}x{height}, Mode: {first_image.mode}")

# Function to check if two colors are similar within a tolerance
def colors_are_similar(color1, color2, tolerance=0):
    r1, g1, b1, a1 = color1
    r2, g2, b2, a2 = color2
    return (abs(r1 - r2) <= tolerance and
            abs(g1 - g2) <= tolerance and
            abs(b1 - b2) <= tolerance and
            abs(a1 - a2) <= tolerance)

# Initialize a list to store common pixels
common_pixels = []

# Iterate through each pixel position
for x in range(width):
    for y in range(height):
        # Get the pixel color from the first image
        first_pixel = first_image.getpixel((x, y))

        # Check if the pixel color is similar in all other images
        is_common = True
        for image_file in image_files[1:]:
            try:
                img = Image.open(image_file).convert("RGBA")  # Convert to RGBA
                if img.size != (width, height):
                    print(f"Image {image_file} has different dimensions: {img.size}")
                    is_common = False
                    break
                pixel = img.getpixel((x, y))
                if not colors_are_similar(pixel, first_pixel, tolerance=0):
                    is_common = False
                    break
            except Exception as e:
                print(f"Error loading {image_file}: {e}")
                is_common = False
                break

        # If the pixel is common, add it to the list
        if is_common:
            common_pixels.append((x, y, first_pixel))

# Print the common pixels
print(f"\nFound {len(common_pixels)} common pixels:")
for pixel in common_pixels:
    print(f"Position: ({pixel[0]}, {pixel[1]}), Color: {pixel[2]}")

# Debug: Print pixel values at specific positions for all images
debug_positions = [(10, 10), (20, 20), (30, 30)]  # Example positions to debug
print("\nDebugging pixel values:")
for x, y in debug_positions:
    print(f"\nPixel at ({x}, {y}):")
    for image_file in image_files:
        try:
            img = Image.open(image_file).convert("RGBA")  # Convert to RGBA
            pixel = img.getpixel((x, y))
            print(f"- {image_file}: {pixel}")
        except Exception as e:
            print(f"- {image_file}: Error loading pixel - {e}")

common_pixels_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
draw = ImageDraw.Draw(common_pixels_image)

# Draw the common pixels
for x, y, color in common_pixels:
    draw.point((x, y), fill=color)

# Save or display the image
common_pixels_image.show()
common_pixels_image.save("common_pixels.png")