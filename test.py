import os
from PIL import Image

# Function to resize image if it's not 48x48
def resize_image(image_path):
    with Image.open(image_path) as img:
        if img.size != (48, 48):
            img = img.resize((48, 48))
            img.save(image_path)  # Save the resized image
            print(f'Resized image: {image_path}')

# Function to walk through directories and process images
def process_images(root_dir):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith('.png'):
                file_path = os.path.join(subdir, file)
                resize_image(file_path)

# Example usage
directory = "./assets/images_resized"  # Directory containing original images
process_images(directory)