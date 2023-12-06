""" 

This module contains 

Example:
    

Todo:
    * make image open and save work
"""


import numpy as np
import tifffile
import matplotlib.pyplot as plt
import imagej 
import os
import pims

from scyjava import jimport


def bioformat_opener(filename):
    """Open an nd2 file using pims
    
    Args:
        filename (str): path to the nd2 file
        
    Returns:
        frames (pims.FramesSequence): a sequence of frames
    """
    frames = pims.open(filename)
    return frames


def tiff_saver(frames, file_name):
    """Save a sequence of frames to a tiff file

    Args:
        frames (pims.FramesSequence): a sequence of frames
        file_name (str): path to the tiff file
    """
    with tifffile.TiffWriter(file_name) as tiff:
        for img in frames:
            tiff.write(img)

            
# v = pims.TiffStack('tiff_stack.tif')
