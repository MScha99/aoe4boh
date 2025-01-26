from PIL import Image
import os

def resize_and_convert_images(input_dir, output_dir, scale_factor=0.5, format="png"):
    """
    Resize and convert all images in the input directory (and its subdirectories)
    to the specified format and save them in the output directory.

    :param input_dir: Path to the directory containing the original images.
    :param output_dir: Path to the directory where resized/converted images will be saved.
    :param scale_factor: Scaling factor (e.g., 0.5 for 50% size).
    :param format: Output format (e.g., "webp", "png", "jpeg").
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Walk through all subdirectories in the input directory
    for root, dirs, files in os.walk(input_dir):
        for filename in files:
            if filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                # Get the full path of the input image
                input_path = os.path.join(root, filename)

                # Calculate the relative path to preserve the directory structure
                relative_path = os.path.relpath(root, input_dir)
                output_subdir = os.path.join(output_dir, relative_path)

                # Create the output subdirectory if it doesn't exist
                if not os.path.exists(output_subdir):
                    os.makedirs(output_subdir)

                # Open the image
                with Image.open(input_path) as img:
                    # Calculate the new size
                    width, height = img.size
                    new_width = int(width * scale_factor)
                    new_height = int(height * scale_factor)

                    # Resize the image
                    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                    # Save the resized image in the specified format
                    output_filename = os.path.splitext(filename)[0] + f".{format}"
                    output_path = os.path.join(output_subdir, output_filename)

                    # Preserve transparency if the image has an alpha channel
                    if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
                        resized_img.save(output_path, format=format, lossless=True)
                    else:
                        resized_img.save(output_path, format=format)

                    print(f"Resized and saved: {output_path}")

# Example usage
input_dir = "E:/Projekty/aoe4boh/assets/images"  # Directory containing original images
output_dir = "E:/Projekty/aoe4boh/assets/images_resized"  # Directory to save resized images
resize_and_convert_images(input_dir, output_dir, scale_factor=0.5, format="png")