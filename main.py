import math
import wave
import os
from pydub import AudioSegment
import matplotlib.pyplot as plt
import serial

#### Teams can add helper functions
#### Add all helper functions here
import struct
import pandas as pd
from sklearn import svm
from pandas import DataFrame
#from pyAudioAnalysis import audioFeatureExtraction
from pyAudioAnalysis import ShortTermFeatures



from features import *
##from feature_helper import estimated_f0, harmonics
##from utils import stft, plot_spectrum, plot_time_domain,read_all_wavedata,plot_feature
import wave
import struct

import numpy as np
import os
##from sklearn import preprocessing
##from sklearn.svm import SVC
##from sklearn.grid_search import GridSearchCV
##from sklearn.ensemble import RandomForestClassifier
##from sklearn.neighbors import KNeighborsClassifier
##from sklearn import cross_validation
##from sklearn.metrics import confusion_matrix
##from sklearn.decomposition import PCA
##from sklearn.externals import joblib
##import pandas as pd
##from sklearn.svm import NuSVC
##from sklearn.neural_network import MLPClassifier
##from sklearn.metrics import classification_report,confusion_matrix
##import sklearn.model_selection 
##from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
##from sklearn.tree import DecisionTreeClassifier


##from Feature_value import Feature_value
##from freqFind import freqFind
##from  inst_detect import inst_detect
from  Instrument_identify import Instrument_identify
##from  onset_notes import onset_notes
##from  Serial_communication import Serial_communication



if __name__ == "__main__":

	#   Instructions
	#   ------------
	#   Do not edit this function.

	# code for checking output for single audio file
	path = os.getcwd()

	#audio_test_all Practice_audio_file
	file_name = path +"\\Practice_audio_file.wav"
	#audio_file = wave.open(file_name)
	
	Instruments, Detected_Notes, Onsets = Instrument_identify(file_name)

	print("\n\tInstruments = "  + str(Instruments))
	print("\n\tDetected Notes = " + str(Detected_Notes))
	print("\n\tOnsets = " + str(Onsets))

	
	Serial_communication()
	
	
	

