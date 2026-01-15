#!/usr/bin/env python3

import os
import sys
import time
import random
import glob
import subprocess
import argparse
import pathlib
from PIL import Image
from inky.auto import auto

# Configuration
DISPLAY_DURATION = 180  # 3 minutes
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLOTS_DIR = os.path.join(ROOT_DIR, 'plots', 'output')
QUOTE_GENERATOR = os.path.join(ROOT_DIR, 'plots', 'generate_quote.py')
QUOTE_IMAGE_NAME = "inspirational_quote.png"

def get_plot_images():
    """Returns a list of all PNG files in the plots output directory, excluding the quote image."""
    all_images = glob.glob(os.path.join(PLOTS_DIR, "*.png"))
    # Filter out the quote image so it doesn't appear in the regular rotation
    return [img for img in all_images if os.path.basename(img) != QUOTE_IMAGE_NAME]

def generate_new_quote():
    """Runs the generate_quote.py script to create a new inspirational quote image."""
    print("Generating new inspirational quote...")
    try:
        subprocess.run([sys.executable, QUOTE_GENERATOR], check=True, cwd=ROOT_DIR)
        return os.path.join(PLOTS_DIR, QUOTE_IMAGE_NAME)
    except subprocess.CalledProcessError as e:
        print(f"Error generating quote: {e}")
        return None

def display_image(inky, image_path, saturation=1.0):
    """Displays the image at image_path on the inky display."""
    print(f"Displaying: {os.path.basename(image_path)}")
    try:
        image = Image.open(image_path)
        resizedimage = image.resize(inky.resolution)
        
        try:
            inky.set_image(resizedimage, saturation=saturation)
        except TypeError:
            inky.set_image(resizedimage)
        
        inky.show()
    except Exception as e:
        print(f"Error displaying image {image_path}: {e}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--saturation", "-s", type=float, default=0.7, help="Colour palette saturation")
    args, _ = parser.parse_known_args()
    
    try:
        inky = auto(ask_user=True, verbose=True)
    except Exception as e:
        print(f"Error initializing Inky: {e}")
        sys.exit(1)

    playlist = []
    counter = 0

    print(f"Starting slideshow loop. Updates every {DISPLAY_DURATION} seconds.")

    while True:
        counter += 1
        
        # Every 5th image, generate and show a quote
        if counter % 5 == 0:
            quote_path = generate_new_quote()
            if quote_path and os.path.exists(quote_path):
                display_image(inky, quote_path, saturation=args.saturation)
            else:
                print("Failed to display quote, skipping.")
        else:
            # Regular plot rotation
            if not playlist:
                playlist = get_plot_images()
                if not playlist:
                    print("No plot images found in output directory. Waiting...")
                    time.sleep(60)
                    continue
                random.shuffle(playlist)
                print(f"Refilled playlist with {len(playlist)} images.")
            
            next_image = playlist.pop()
            display_image(inky, next_image, saturation=args.saturation)
        
        time.sleep(DISPLAY_DURATION)

if __name__ == "__main__":
    main()