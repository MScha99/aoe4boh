from data import worker_location_on_screen, resource_location_on_screen

# Combine all regions into a single list
all_regions = list(worker_location_on_screen.values()) + list(resource_location_on_screen.values())

# Calculate the bounding box for the initial crop (in percentages)
left = min(region["x"] for region in all_regions)
top = min(region["y"] for region in all_regions)
right = max(region["x"] + region["width"] for region in all_regions)
bottom = max(region["y"] + region["height"] for region in all_regions)

# Define the initial crop region (in percentages)
initial_crop = {
    "x": left,
    "y": top,
    "width": right - left,
    "height": bottom - top
}

# Function to recalculate coordinates relative to the cropped image
def recalculate_coordinates(regions, initial_crop):
    left = initial_crop["x"]
    top = initial_crop["y"]
    crop_width = initial_crop["width"]
    crop_height = initial_crop["height"]
    recalculated_regions = {}
    for key, region in regions.items():
        recalculated_regions[key] = {
            "x": ((region["x"] - left) / crop_width) * 100,  # Recalculate x as % of cropped width
            "y": ((region["y"] - top) / crop_height) * 100,  # Recalculate y as % of cropped height
            "width": (region["width"] / crop_width) * 100,   # Recalculate width as % of cropped width
            "height": (region["height"] / crop_height) * 100 # Recalculate height as % of cropped height
        }
    return recalculated_regions

# Recalculate worker and resource coordinates
worker_location_on_screen_cropped = recalculate_coordinates(worker_location_on_screen, initial_crop)
resource_location_on_screen_cropped = recalculate_coordinates(resource_location_on_screen, initial_crop)

# Print the recalculated coordinates
print("Initial Crop Region (percentages):", initial_crop)
print("\nRecalculated Worker Locations (percentages of cropped region):")
for key, region in worker_location_on_screen_cropped.items():
    print(f"{key}: {region}")

print("\nRecalculated Resource Locations (percentages of cropped region):")
for key, region in resource_location_on_screen_cropped.items():
    print(f"{key}: {region}")