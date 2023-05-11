#!/bin/bash

# set variables for data and settings paths
# DATA_PATH="/Users/nelsschimek/Downloads/010623_HT002_upper_right_v2.tif"
# SETTINGS_PATH="/Users/nelsschimek/Documents/nancelab/pytrackmate/models/trackmate/basic_settings.xml"

# run the new script
ImageJ-linux64 --ij2 --headless --console --memory=$MEMORY /read_settings_and_process_mpt_tiff.py #--input_path $DATA_PATH --settings_file $SETTINGS_PATH