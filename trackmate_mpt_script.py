# import sys
import os
import imagej
import scyjava as sj
# import random
sj.config.add_options('-Xmx6g')

os.environ["JAVA_HOME"] = "/Users/nelsschimek/mambaforge/envs/i2k-2022-pyimagej/"

# initialize ImageJ
ij = imagej.init('/Applications/Fiji.app/')
print(f"ImageJ version: {ij.getVersion()}")

plga_peg_image_path = "/Users/nelsschimek/Documents/nancelab/diff_classifier/notebooks/development/MPT_Data/P10F_NT_10DIV_40nm_slice_2_midbrain_vid_2_0_0.tif"
plga_peg_image = ij.io().open(plga_peg_image_path)

print(
    f" dims: {plga_peg_image.dims if hasattr(plga_peg_image, 'dims') else 'N/A'}")

Model = sj.jimport('fiji.plugin.trackmate.Model')
Settings = sj.jimport('fiji.plugin.trackmate.Settings')
TrackMate = sj.jimport('fiji.plugin.trackmate.TrackMate')
FeatureFilter = sj.jimport('fiji.plugin.trackmate.features.FeatureFilter')
LAPUtils = sj.jimport('fiji.plugin.trackmate.tracking.jaqaman.LAPUtils')
SelectionModel = sj.jimport('fiji.plugin.trackmate.SelectionModel')
Logger = sj.jimport('fiji.plugin.trackmate.Logger')
DisplaySettingsIO = sj.jimport(
    'fiji.plugin.trackmate.gui.displaysettings.DisplaySettingsIO')
HyperStackDisplayer = sj.jimport(
    'fiji.plugin.trackmate.visualization.hyperstack.HyperStackDisplayer')

DogDetectorFactory = sj.jimport(
    'fiji.plugin.trackmate.detection.DogDetectorFactory')
SparseLAPTrackerFactory = sj.jimport(
    'fiji.plugin.trackmate.tracking.jaqaman.SparseLAPTrackerFactory')

model = Model()

model.setLogger(Logger.IJ_LOGGER)

imp = ij.py.to_imageplus(plga_peg_image)


print('Done!')
