"""
This script runs a single video through automated trackmate tracking
"""
import sys
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

dims = imp.getDimensions() # default order: XYCZT

if dims[4] == 1:
    print('need to change order')
    imp.setDimensions(dims[4], dims[3], dims[2])

settings = Settings(imp)
# Configure detector
settings.detectorFactory = DogDetectorFactory()
settings.detectorSettings = {
    'DO_SUBPIXEL_LOCALIZATION' : False,
    'RADIUS' : 6.0,
    'TARGET_CHANNEL': ij.py.to_java(1),
    'DO_MEDIAN_FILTERING': True,
    'THRESHOLD': 0.0
}

# Configure tracker
settings.trackerFactory = SparseLAPTrackerFactory()
settings.trackerSettings = LAPUtils.getDefaultSegmentSettingsMap()
settings.trackerSettings['LINKING_MAX_DISTANCE'] = 15.0
settings.trackerSettings['GAP_CLOSING_MAX_DISTANCE'] = 20.0
settings.trackerSettings['MAX_FRAME_GAP'] = ij.py.to_java(6)

trackmate = TrackMate(model, settings)
ok = trackmate.checkInput()
if not ok:
    sys.exit(str(trackmate.getErrorMessage()))

ok = trackmate.process()
if not ok:
    sys.exit(str(trackmate.getErrorMessage()))

model.getLogger().log('Found ' + str(model.getTrackModel().nTracks(True)) + ' tracks.')


print('Done!')
