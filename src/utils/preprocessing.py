""" 

This module contains 

Example:

Known issues:
    * https://github.com/soft-matter/pims/issues/432 
        pim's bioformat downloader is broken, use nd2reader as workaround
    

Todo:
    * make image open and save work
"""


import numpy as np
import tifffile
import matplotlib.pyplot as plt
import imagej 
import os
from nd2reader import ND2Reader
from scyjava import jimport
from PIL import Image


def bioformat_opener(filename):
    """Open an nd2 file using nd2reader - pims currently is buggy
    
    Args:
        filename (str): path to the nd2 file
        
    Returns:
        ND2Reader: a reader object
    """
    if not os.path.isfile(filename):
        raise FileNotFoundError("File not found: {}".format(filename))
    return ND2Reader(filename)


def tiff_saver(frames, file_name):
    """Save a sequence of frames to a tiff file

    Args:
        frames (list): list of frames to save
        file_name (str): path to the tiff file
    """
    with tifffile.TiffWriter(file_name) as tiff:
        for img in frames:
            tiff.write(img)


def convert_to_png(tiff_frames, png_file_name):
    """Convert a sequence of frames to a png file

    Args:
        tiff_frames (list): list of frames to save
        png_file_name (str): path to the png file
    """
    # with Image.open(tiff_frames) as im:
    #     im.save(png_file_name, format='png')
    for i, frame in enumerate(tiff_frames):
        frame = frame.astype(np.uint16)
        im = Image.fromarray(frame)
        im.save(f"{png_file_name}/{i}.png", format='png')

            
# v = pims.TiffStack('tiff_stack.tif')

if __name__ == "__main__":
    # tiff_saver(bioformat_opener('static_volume/Slide1-6_Region0007_Channel555 nm,395 nm_Seq0050.nd2'), "static_volume/test.tif")
    convert_to_png(bioformat_opener('static_volume/Slide1-6_Region0007_Channel555 nm,395 nm_Seq0050.nd2'), "static_volume")
