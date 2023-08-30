import sys
import os
#from pathlib import Path

# if len(sys.argv) != 3:
#     print("Usage: python read_settings_and_process_tiff_stack.py <data_folder_path> <settings_file_path>")
#     sys.exit(1)

# data_folder = Path(sys.argv[1])
# settings_file = Path(sys.argv[2])

from java.io import File
from java.lang import System

from ij import IJ, ImagePlus
from ij.io import Opener

from fiji.plugin.trackmate import TrackMate
from fiji.plugin.trackmate import Logger
from fiji.plugin.trackmate.io import TmXmlReader, TmXmlWriter

from fiji.plugin.trackmate.tracking import ManualTrackerFactory

from fiji.plugin.trackmate import Model
from fiji.plugin.trackmate import Settings
from fiji.plugin.trackmate import TrackMate
from fiji.plugin.trackmate import SelectionModel
from fiji.plugin.trackmate.detection import LogDetectorFactory
from fiji.plugin.trackmate.tracking.sparselap import SimpleSparseLAPTrackerFactory
from fiji.plugin.trackmate.gui.displaysettings import DisplaySettingsIO
import fiji.plugin.trackmate.visualization.hyperstack.HyperStackDisplayer as HyperStackDisplayer
import fiji.plugin.trackmate.features.FeatureFilter as FeatureFilter


# We have to do the following to avoid errors with UTF8 chars generated in
# TrackMate that will mess with our Fiji Jython.
reload(sys)
sys.setdefaultencoding("utf-8")

# -----------------
# Read data stack
# -----------------

#srcpath = '/Users/nelsschimek/Documents/nancelab/pytrackmate/data/Healthy-QD-BEVs-Video3_0_1.tif'

#print('uisng constructor')
#imp1 = ImagePlus(srcpath)

# print('using IJ static method')
# imp2 = IJ.openImage(srcpath)

# print('Using Opener class')
# imp3 = Opener().openImage(srcpath)

# print("reading data from: " + srcpath)
imp = IJ.openImage("/mmfs1/home/at007/pytrackmate/pytrackmate/slice_1_vid_1.tif")
#imp = IJ.openImage(data_path)
print("data read successfully")

model = Model()

# Send all messages to ImageJ log window.
model.setLogger(Logger.IJ_LOGGER)



#------------------------
# Prepare settings object
#------------------------

settings = Settings(imp)

# Configure detector - We use the Strings for the keys
settings.detectorFactory = LogDetectorFactory()
settings.detectorSettings = {
    'DO_SUBPIXEL_LOCALIZATION' : False, #turn to false
    'RADIUS' : 6.0,
    'TARGET_CHANNEL' : 1,
    'THRESHOLD' : 0.,
    'DO_MEDIAN_FILTERING' : False,
}

# Configure spot filters - Classical filter on quality
filter1 = FeatureFilter('QUALITY', 2.7, True)
settings.addSpotFilter(filter1)

# Configure tracker - We want to allow merges and fusions
settings.trackerFactory =  SimpleSparseLAPTrackerFactory() # check this
settings.trackerSettings = settings.trackerFactory.getDefaultSettings() # almost good enough
settings.trackerSettings['ALLOW_TRACK_SPLITTING'] = False
settings.trackerSettings['ALLOW_TRACK_MERGING'] = False

# Add ALL the feature analyzers known to TrackMate. They will
# yield numerical features for the results, such as speed, mean intensity etc.
settings.addAllAnalyzers()

# Configure track filters - We want to get rid of the two immobile spots at
# the bottom right of the image. Track displacement must be above 10 pixels.

#filter2 = FeatureFilter('TRACK_DISPLACEMENT', 10, True)
#settings.addTrackFilter(filter2)


#-------------------
# Instantiate plugin
#-------------------

trackmate = TrackMate(model, settings)

#--------
# Process
#--------

ok = trackmate.checkInput()
if not ok:
    sys.exit(str(trackmate.getErrorMessage()))

ok = trackmate.process()
if not ok:
    sys.exit(str(trackmate.getErrorMessage()))


#----------------
# Display results
#----------------

# A selection.
selectionModel = SelectionModel( model )

# Read the default display settings.
# ds = DisplaySettingsIO.readUserDefault()

# displayer =  HyperStackDisplayer( model, selectionModel, imp, ds )
# displayer.render()
# displayer.refresh()

# Echo results with the logger we set at start:
model.getLogger().log( str( model ) )
fm = model.getFeatureModel()

for id in model.getTrackModel().trackIDs(True):

    # Fetch the track feature from the feature model.
    v = fm.getTrackFeature(id, 'TRACK_MEAN_SPEED')
    model.getLogger().log('')
    model.getLogger().log('Track ' + str(id) + ': mean velocity = ' + str(v) + ' ' + model.getSpaceUnits() + '/' + model.getTimeUnits())

        # Get all the spots of the current track.
    track = model.getTrackModel().trackSpots(id)
    for spot in track:
        sid = spot.ID()
        # Fetch spot features directly from spot.
        # Note that for spots the feature values are not stored in the FeatureModel
        # object, but in the Spot object directly. This is an exception; for tracks
        # and edges, you have to query the feature model.
        x=spot.getFeature('POSITION_X')
        y=spot.getFeature('POSITION_Y')
        t=spot.getFeature('FRAME')
        q=spot.getFeature('QUALITY')
        snr=spot.getFeature('SNR_CH1')
        mean=spot.getFeature('MEAN_INTENSITY_CH1')
        model.getLogger().log('\tspot ID = ' + str(sid) + ': x='+str(x)+', y='+str(y)+', t='+str(t)+', q='+str(q) + ', snr='+str(snr) + ', mean = ' + str(mean))

print("end, Byeeee")
                                            
                                                                 