import sys

from ij import IJ
from ij import WindowManager

from fiji.plugin.trackmate import TrackMate
from fiji.plugin.trackmate import Model
from fiji.plugin.trackmate import SelectionModel
from fiji.plugin.trackmate import Settings
from fiji.plugin.trackmate import Logger

# We have to do the following to avoid errors with UTF8 chars generated in 
# TrackMate that will mess with our Fiji Jython.
reload(sys)
sys.setdefaultencoding('utf-8')


imp = IJ.openImage('https://fiji.sc/samples/FakeTracks.tif')
imp.show()


#-------------------------
# Instantiate model object
#-------------------------

model = Model()


#------------------------
# Prepare settings object
#------------------------

settings = Settings(imp)


#----------------------
# Instantiate trackmate
#----------------------

trackmate = TrackMate(model, settings)

