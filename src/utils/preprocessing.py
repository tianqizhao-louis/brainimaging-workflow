""" 

This module contains 

Example:
    

Todo:
    * make image open and save work
"""


import numpy as np
import nd2reader
import tifffile
import matplotlib.pyplot as plt
import imagej 
import os
from scyjava import jimport


def convert_nd2_to_tiff(nd2_filename, tiff_filename):
    with nd2reader.ND2Reader(nd2_filename) as images:

        print(images.metadata)


        # Number of channels in the ND2 file
        num_channels = images.sizes['C'] if 'C' in images.sizes else 1
        
        # If there are multiple channels, assume they correspond to RGB and stack them
        if num_channels > 1:
            # Collect each channel's images
            channels = [images[channel] for channel in range(num_channels)]
            
            # Transpose and stack the channels
            rgb_images = [np.stack([channels[j][i] for j in range(num_channels)], axis=-1) for i in range(len(channels[0]))]
            
            with tifffile.TiffWriter(tiff_filename) as tiff:
                for img in rgb_images:
                    tiff.save(img)
        else:
            pass
            # If only one channel, save as grayscale
            with tifffile.TiffWriter(tiff_filename) as tiff:
                for img in images:
                    tiff.write(img)


def convert_nd2_to_tiff_2(nd2_filename, tiff_filename):
    """
    Convert an ND2 file to a TIFF file.
    
    Args:
        nd2_filename (str): The path to the ND2 file.
        tiff_filename (str): The path to the TIFF file.
        
    Returns:
        None
    """
    # ij = imagej.init(headless=True)
    # image = ij.io().open(nd2_filename)
    # ij.io().save(image, tiff_filename)
    # print('Saved TIFF file to {}'.format(tiff_filename))
    ij = imagej.init('sc.fiji:fiji', mode='headless')
    print(f"ImageJ version: {ij.getVersion()}")
    # image = ij.io().open(nd2_filename)
    # ij.io().save(image, tiff_filename)
    # print('Saved TIFF file to {}'.format(tiff_filename))

    dataset = ij.io().open(tiff_filename)
    dump_info(dataset)


def dump_info(image):
    """A handy function to print details of an image object."""
    name = image.name if hasattr(image, 'name') else None # xarray
    if name is None and hasattr(image, 'getName'): name = image.getName() # Dataset
    if name is None and hasattr(image, 'getTitle'): name = image.getTitle() # ImagePlus
    print(f" name: {name or 'N/A'}")
    print(f" type: {type(image)}")
    print(f"dtype: {image.dtype if hasattr(image, 'dtype') else 'N/A'}")
    print(f"shape: {image.shape}")
    print(f" dims: {image.dims if hasattr(image, 'dims') else 'N/A'}")


if __name__ == '__main__':
    # Read the .nd2 file
    nd2_filename = 'static_volume/Slide1-6_Region0007_Channel555 nm,395 nm_Seq0050.nd2'
    tiff_filename = 'static_volume/test.tif'
    convert_nd2_to_tiff_2(nd2_filename, tiff_filename)

    # convert_nd2_to_tiff(nd2_filename, tiff_filename)

    # # # print files and directors from the root directory
    # # # ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    # # # print(ROOT_DIR)
    # # for root, dirs, files in os.walk("/app/data"):
    # #     for filename in files:
    # #         print(filename)
    # #     for dirname in dirs:
    # #         print(dirname)

    # # with nd2reader.ND2Reader(nd2_filename) as images:
    # #     # plt.imshow(images[0])
    # #     plt.imshow(images[0], cmap=plt.cm.coolwarm)
    # #     plt.show()
    # # convert_nd2_to_tiff_2(nd2_filename, tiff_filename)
    # ij = imagej.init('sc.fiji:fiji', mode='headless')
    # array = np.random.rand(5, 4, 3)
    # dataset = ij.py.to_java(array)

    # print(dataset.shape)

    # System = jimport('java.lang.System')
    # print(f"ImageJ version: {ij.getVersion()}")

    # Runtime = jimport('java.lang.Runtime')
    # print(Runtime.getRuntime().maxMemory() // (2**20), " MB available to Java")
