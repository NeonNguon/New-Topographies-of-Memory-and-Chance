# this version is focusing on changing the distribution of coordinates towards the center of the map 

import tkinter as tk
from tkinter import messagebox
import random
from shapely.geometry import Point, Polygon, MultiPolygon
import pyperclip
import json
import sys
import os
import hashlib

def get_hashed_seed(number):
    # returns a deterministic but well-spread seed for a 6-digit number
    hashval = hashlib.md5(str(number).encode()).hexdigest()
    return int(hashval[:8], 16)  # convert first 8 hex digits to integer

# Helper for PyInstaller resource path
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # When running in a PyInstaller bundle
        base_path = sys._MEIPASS
    except AttributeError:
        # When running in a normal Python environment
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Load the coordinates from the JSON file
with open(resource_path('ho_chi_minh_city_coords.json'), 'r', encoding='utf-8') as f:
    all_coords = json.load(f)

# The JSON file contains a list of lists of coordinate pairs
# Each coordinate pair is [latitude, longitude]

# Create a list of Polygons
polygons = []
for coords_latlon in all_coords:
    coords_lonlat = [tuple([coord[1], coord[0]]) for coord in coords_latlon]
    poly = Polygon(coords_lonlat)
    polygons.append(poly)

# Create a MultiPolygon if there are multiple polygons
if len(polygons) > 1:
    polygon = MultiPolygon(polygons)
else:
    polygon = polygons[0]

centroid = polygon.centroid


# Function to generate random coordinate within Ho Chi Minh City based on a seed
def generate_random_coordinate(seed):
    minx, miny, maxx, maxy = polygon.bounds
    center_x, center_y = centroid.x, centroid.y
    random.seed(get_hashed_seed(seed))
    stddev_x = (maxx - minx) / 12 # spread controls
    stddev_y = (maxy - miny) / 12
    tries = 0
    while True:
        # Gaussian around the centroid, with a reasonably large stddev
        x = random.gauss(center_x, stddev_x)
        y = random.gauss(center_y, stddev_y)
        pnt = Point(x, y)
        tries += 1
        if polygon.contains(pnt):
            return (pnt.y, pnt.x)
        # fallback to uniform if we try too often
        if tries > 1000:
            x = random.uniform(minx, maxx)
            y = random.uniform(miny, maxy)
            pnt = Point(x, y)
            if polygon.contains(pnt):
                return (pnt.y, pnt.x)

# Function to generate GPS coordinates and copy to clipboard
def generate_and_copy_coordinates():
    try:
        six_figure_number = int(entry.get())
        latitude, longitude = generate_random_coordinate(six_figure_number)
        coordinates = f"{longitude:.6f}, {latitude:.6f}"
        pyperclip.copy(coordinates)
        output_label.config(text=f"Generated GPS Coordinates: {coordinates}\nCopied to clipboard.")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid six-figure number.")

# Create the main window
root = tk.Tk()
root.title("GPS Coordinate Generator")

# Create and place the widgets
tk.Label(root, text="Enter a six-figure number:").grid(row=0, column=0, padx=10, pady=10)
entry = tk.Entry(root)
entry.grid(row=0, column=1, padx=10, pady=10)

generate_button = tk.Button(root, text="Generate and Copy", command=generate_and_copy_coordinates)
generate_button.grid(row=1, column=0, columnspan=2, pady=10)

output_label = tk.Label(root, text="")
output_label.grid(row=2, column=0, columnspan=2, pady=10)

# Start the main event loop
root.mainloop()
