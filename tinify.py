import os
from PIL import Image
from PIL import ExifTags

# Ask the user for the input directory
INPUT_DIR = input("Enter the input directory path: ")

# Ensure the input directory exists
if not os.path.isdir(INPUT_DIR):
    print(f"The specified input directory '{INPUT_DIR}' does not exist.")
    exit()

# Ask the user for the desired width
try:
    WIDTH = int(input("Enter the desired width for resizing: "))
except ValueError:
    print("Invalid input for width. Please enter a valid integer.")
    exit()

# Use the same directory for the output
OUTPUT_DIR = INPUT_DIR

# Create a list of supported image file extensions
SUPPORTED_EXTENSIONS = [".jpg", ".webp", ".jpeg", ".png"]

# Initialize variables to keep track of statistics
total_files_processed = 0

# Iterate over all files in the input directory
for filename in os.listdir(INPUT_DIR):
    # Get the file extension
    extension = os.path.splitext(filename)[1]

    # Convert the extension to lowercase
    extension = extension.lower()

    # Check if the file extension is supported
    if extension in SUPPORTED_EXTENSIONS:
        # Check if the file already has _tiny in the name
        if "_tiny" not in filename:
            # Split the filename into the basename and extension
            basename, extension = os.path.splitext(filename)

            # Create the new filename with the _tiny suffix before the extension
            new_filename = f"{basename}_tiny{extension}"

            # Open the image file
            image = Image.open(os.path.join(INPUT_DIR, filename))

            # Check for and correct image rotation using EXIF data
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    try:
                        exif = dict(image._getexif().items())
                        if exif[orientation] == 3:
                            image = image.rotate(180, expand=True)
                        elif exif[orientation] == 6:
                            image = image.rotate(270, expand=True)
                        elif exif[orientation] == 8:
                            image = image.rotate(90, expand=True)
                    except (AttributeError, KeyError, IndexError):
                        # Ignore any exceptions if EXIF data doesn't exist or is corrupted
                        pass

            # Calculate the new height based on the aspect ratio
            height = int(image.height * (WIDTH / image.width))

            # Resize the image without specifying the rotate argument
            resized_image = image.resize((WIDTH, height), Image.LANCZOS)

            # Save the resized image to the output directory
            output_image_path = os.path.join(OUTPUT_DIR, new_filename)
            resized_image.save(output_image_path)

            # Update statistics
            total_files_processed += 1

            # Print a message with file details
            print(f"Processed: {filename}")
            print(f"Saved as: {new_filename}\n")

# Print summary statistics
print(f"Total Files Processed: {total_files_processed}")
