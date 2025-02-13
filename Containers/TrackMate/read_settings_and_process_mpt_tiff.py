import sys
import os
import json
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
from fiji.plugin.trackmate.detection import LogDetectorFactory
from fiji.plugin.trackmate.tracking.sparselap import SparseLAPTrackerFactory
from fiji.plugin.trackmate.gui.displaysettings import DisplaySettingsIO
import fiji.plugin.trackmate.visualization.hyperstack.HyperStackDisplayer as HyperStackDisplayer
import fiji.plugin.trackmate.features.FeatureFilter as FeatureFilter
from fiji.plugin.trackmate.detection import DogDetectorFactory
from fiji.plugin.trackmate.util import TMUtils

# We have to do the following to avoid errors with UTF8 chars generated in
# TrackMate that will mess with our Fiji Jython.
reload(sys)
sys.setdefaultencoding("utf-8")

class ImageProcessor:
    def __init__(self, settings_path, output_path):
        self.model = Model()
        self.model.setLogger(Logger.IJ_LOGGER)
        self.settings_path = settings_path
        self.output_path = output_path
        self.track_data_filename = None
        self.spot_data_filename = None
        
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
        
    def load_image(self):
        self.imp = IJ.openImage(self.image_path)
        IJ.run(self.imp, "Properties...", "channels=1 slices=1 frames=651 unit=pixel pixel_width=1.0000 pixel_height=1.0000 voxel_depth=1.0000");

    def load_settings(self):
        self.settings = Settings(self.imp)
        
        with open(self.settings_path) as f:
            self.settings_json = json.load(f)
             
        self.settings.detectorFactory = DogDetectorFactory()
        self.settings.detectorSettings = self.settings_json["detectorSettings"]
        
        #filter1 = FeatureFilter('QUALITY', self.settings_json["quality"], True)
        #self.settings.addSpotFilter(filter1)

        self.settings.trackerFactory = SparseLAPTrackerFactory()
        self.settings.trackerSettings = self.settings.trackerFactory.getDefaultSettings()
        self.settings.trackerSettings.update(self.settings_json["trackerSettings"])
        print(self.settings.trackerSettings)

        self.settings.addAllAnalyzers()
        
    def process_image(self, image_path):
        self.image_path = image_path
        self.load_image()
        self.load_settings()
        self.trackmate = TrackMate(self.model, self.settings)
        self.verify_trackmate()
        
        #self.model.getLogger().log('Found ' + str(self.model.getTrackModel().nTracks(True)) + ' tracks.')
        self.selectionModel = SelectionModel(self.model)
        self.featureModel = self.model.getFeatureModel()
        
        image_name = os.path.splitext(os.path.basename(self.image_path))[0]
        self.track_data_filename = os.path.join(self.output_path, image_name + "_track_data.csv")
        self.spot_data_filename = os.path.join(self.output_path, image_name + "_spot_data.csv")
        with open(self.track_data_filename, 'w') as track_file, open(self.spot_data_filename, 'w') as spot_file:
            self.track_file = track_file
            self.spot_file = spot_file
            track_file.write("TRACK_ID,MEAN_SPEED\n")
            spot_file.write("TRACK_ID,ID,POSITION_X,POSITION_Y,FRAME,QUALITY,SNR_CH1,MEAN_INTENSITY_CH1\n")
            for track_id in self.model.getTrackModel().trackIDs(True):
                self.process_track(track_id)
            


                
        self.track_file = None
        self.spot_file = None
                
    def process_track(self, track_id):
        v = self.featureModel.getTrackFeature(track_id, 'TRACK_MEAN_SPEED')
        # self.model.getLogger().log('')
        # self.model.getLogger().log('Track ' + str(track_id) + ': mean velocity = ' + str(v) + ' ' + self.model.getSpaceUnits() + '/' + self.model.getTimeUnits())
        self.track_file.write(str(track_id) + "," + str(v) + "\n")
        
        track = self.model.getTrackModel().trackSpots(track_id)
        for spot in track:
            self.process_spot(spot, track_id)
            
    def process_spot(self, spot, track_id):
        sid = spot.ID()
        x = spot.getFeature('POSITION_X')
        y = spot.getFeature('POSITION_Y')
        t = spot.getFeature('FRAME')
        q = spot.getFeature('QUALITY')
        snr = spot.getFeature('SNR_CH1')
        mean = spot.getFeature('MEAN_INTENSITY_CH1')
        # self.model.getLogger().log('\tspot ID = ' + str(sid) + ': x='+str(x)+', y='+str(y)+', t='+str(t)+', q='+str(q) + ', snr='+str(snr) + ', mean = ' + str(mean))
        self.spot_file.write(str(track_id) + "," + str(sid) + "," + str(x) + "," + str(y) + "," + str(t) + "," + str(q) + "," + str(snr) + "," + str(mean) + "\n")
                    
    def verify_trackmate(self):
        ok = self.trackmate.checkInput()
        if not ok:
            sys.exit(str(self.trackmate.getErrorMessage()))
        ok = self.trackmate.process()
        if not ok:
            sys.exit(str(self.trackmate.getErrorMessage())) 
            
    def process_directory(self, directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            print("Processing image: " + file_path)
            try:
                self.process_image(file_path)
            except Exception as e:
                print("Error processing image: " + file_path)
                print(e)
            

    def plot_spot_quality_histogram(self):

        quality_list = []

        all_spots = self.model.getTrackModel().getSpots()
        for spot in all_spots:
            quality = spot.getFeature('QUALITY')
            quality_list.append(quality)

        n_bins = TMUtils.getNBins(quality_list)
        hist = TMUtils.hist(quality_list, n_bins)
        auto_quality = TMUtils.otsuThreshold(quality_list, n_bins)

                   
    
image_processor = ImageProcessor("settings.json", "./output/agarose")
image_processor.process_directory("./images/agarose")
print("end, Byeeee")
