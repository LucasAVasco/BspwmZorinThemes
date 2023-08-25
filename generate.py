#!/bin/env python3


"""
Generate all theme correction themes.

These themes only correct Zorin OS themes to work with BSPWM window manager.

Parameters:
    - $1: Path to folder where Zorin OS themes are saved.
    - $2: Path to folder where to save correction themes.
"""

import sys
import os
import shutil
import re


zorin_themes_path = sys.argv[1]
correction_themes_path = sys.argv[2]

themes_colors = [
            "Blue",
            "Green",
            "Grey",
            "Orange",
            "Purple",
            "Red",
        ]

correction_themes_files = [
        "gtk-2.0/gtkrc",
        "gtk-3.0/gtk-dark.css",
        "gtk-3.0/gtk.css",
        "index.theme"
        ]



for color in themes_colors:
    for light in ["Light", "Dark"]:
        # Name of themes (original and correction)
        Zorin_theme_name = "Zorin" + color + '-' + light
        correction_theme_name = "Bspwm" + Zorin_theme_name

        # Path to new correction theme folder
        correction_path = correction_themes_path + '/' + correction_theme_name + '/'
        correction_path = re.sub("//", '/', correction_path)  # Removes double slash

        # Removes the correction theme folder if it already exists
        try:
            shutil.rmtree(correction_path)
        except FileNotFoundError:
            pass

        # Creates the directories of the correction theme
        print("\n\nCreating directories of '{}' theme...".format(correction_theme_name))
        os.makedirs(correction_path + "gtk-2.0")
        os.makedirs(correction_path + "gtk-3.0")

        # Copies the themes files, replacing the tags with corresponding values
        for fname in correction_themes_files:
            # There are not "gtk-3.0/gtk-dark.css" file in dark versions of Zorin OS themes
            if fname == "gtk-3.0/gtk-dark.css" and light == "Dark":
                continue

            with open(fname, 'r') as f:
                text = f.read()

                # Replaces tags
                zorin_themes_path = re.sub("//", "/", zorin_themes_path)
                text = re.sub("<THEME_NAME>", Zorin_theme_name, text)
                text = re.sub("<ZORIN_THEMES_PATH>", zorin_themes_path, text)

                # Writes the text to the correction file
                dest_file_name = correction_path + fname
                with open(dest_file_name, 'w') as dest_file:
                    print("Writing '{}' file.".format(dest_file_name))
                    dest_file.write(text)

