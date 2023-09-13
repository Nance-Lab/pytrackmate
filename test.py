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
from fiji.plugin.trackmate import Model
from fiji.plugin.trackmate import Settings
from fiji.plugin.trackmate import TrackMate
from fiji.plugin.trackmate import SelectionModel
from fiji.plugin.trackmate.tracking.jaqaman import SparseLAPTrackerFactory
import fiji.plugin.trackmate.visualization.hyperstack.HyperStackDisplayer as HyperStackDisplayer
import fiji.plugin.trackmate.features.FeatureFilter as FeatureFilter
from fiji.plugin.trackmate.detection import DogDetectorFactory

quality_values = [2.9, 9]
num_spots_list = []
num_tracks_list = []


for quality_value in quality_values:  # Values from 0 to 10 in increments of 0.1
    # Convert the loop variable to the actual quality value (0.0 to 10.0) 861511 spots. 44
    quality = quality_value
    print("Quality Value: %.1f" % quality)
    imp = IJ.openImage("PBS_control_3_0_1.tif")
    IJ.run(imp, "Properties...", "channels=1 slices=1 frames=651 unit=pixel pixel_width=1.0000 pixel_height=1.0000 voxel_depth=1.0000");
    print("data read successfully")
    model = Model()
    model.setLogger(Logger.IJ_LOGGER)
    settings = Settings(imp)
    settings.detectorFactory = DogDetectorFactory()
    settings.detectorSettings = {
        'DO_SUBPIXEL_LOCALIZATION' : False, #turn to false
        'RADIUS' : 6.0,
        'TARGET_CHANNEL' : 1,
        'THRESHOLD' : 0.0,
        'DO_MEDIAN_FILTERING' : True,
    }  
    filter1 = FeatureFilter('QUALITY', quality, True)
    settings.addSpotFilter(filter1)
    print("quality is now 10")
    settings.trackerFactory = SparseLAPTrackerFactory() # check this
    settings.trackerSettings = settings.trackerFactory.getDefaultSettings() # almost good enough
    settings.trackerSettings['MAX_FRAME_GAP'] = 6
    settings.trackerSettings['ALTERNATIVE_LINKING_COST_FACTOR'] = 1.05
    settings.trackerSettings['LINKING_MAX_DISTANCE'] = 15.0
    settings.trackerSettings['GAP_CLOSING_MAX_DISTANCE'] = 20.0
    settings.trackerSettings['SPLITTING_MAX_DISTANCE'] = 15.0
    settings.trackerSettings['ALLOW_GAP_CLOSING'] = True
    settings.trackerSettings['MERGING_MAX_DISTANCE'] = 15.0
    settings.trackerSettings['CUTOFF_PERCENTILE'] = 0.9
    settings.trackerSettings['ALLOW_TRACK_SPLITTING'] = False
    settings.trackerSettings['ALLOW_TRACK_MERGING'] = False
    settings.addAllAnalyzers()
    trackmate = TrackMate(model, settings)
    ok = trackmate.checkInput()
    if not ok:
        break;
    
    ok = trackmate.process()
    if not ok:
        break;
    selectionModel = SelectionModel( model )
    print("Found: " + str(model.getSpots().getNSpots(True)) + ' Spots.')
    model.getLogger().log('Found ' + str(model.getTrackModel().nTracks(True)) + ' tracks.')
    num_spots_list.append(int(str(model.getSpots().getNSpots(True))))
    num_tracks_list.append(int(str(model.getTrackModel().nTracks(True))))

print(num_spots_list)
print(num_tracks_list)