import sys
import os
from pathlib import Path

# if len(sys.argv) != 3:
#     print("Usage: python read_settings_and_process_tiff_stack.py <data_folder_path> <settings_file_path>")
#     sys.exit(1)

# data_folder = Path(sys.argv[1])
# settings_file = Path(sys.argv[2])

# from java.io import File
# from java.lang import System

# from ij import IJ
# from fiji.plugin.trackmate import TrackMate
# from fiji.plugin.trackmate import Logger
# from fiji.plugin.trackmate.io import TmXmlReader, TmXmlWriter


# We have to do the following to avoid errors with UTF8 chars generated in
# TrackMate that will mess with our Fiji Jython.
reload(sys)
sys.setdefaultencoding("utf-8")

# -----------------
# Read data stack
# -----------------

# Get currently selected image
# imp = WindowManager.getCurrentImage()
# print("reading data from: " + data_folder)
# data_path = "/data/" + os.environ.get("TIFF_STACK")
# print("reading data from: " + data_path)
# # imp = IJ.openImage("https://fiji.sc/samples/FakeTracks.tif")
# imp = IJ.openImage(data_path)
# print("data read successfully")