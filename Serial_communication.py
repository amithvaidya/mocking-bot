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
from feature_helper import estimated_f0, harmonics
from utils import stft, plot_spectrum, plot_time_domain,read_all_wavedata,plot_feature
import wave
import struct

import numpy as np
import os
from sklearn import preprocessing
from sklearn.svm import SVC
from sklearn.grid_search import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import cross_validation
from sklearn.metrics import confusion_matrix
from sklearn.decomposition import PCA
from sklearn.externals import joblib
import pandas as pd
from sklearn.svm import NuSVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report,confusion_matrix
import sklearn.model_selection 
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier


from Feature_value import Feature_value
from freqFind import freqFind
from  inst_detect import inst_detect
from  Instrument_identify import Instrument_identify
from  onset_notes import onset_notes
from  Serial_communication import Serial_communication

def Serial_communication():
    
    ser = serial.Serial()
    pattern='' #consit the 1-dimensional string of onsets and instrument key to be pressed  to be communicated to bot  
    print('Communicating to Bot...')
    flag=0
    for i in Instruments:
        
        if (i=='Piano' ):
            pattern=pattern+'P'+str(Detected_Notes[flag][0])+str(Onsets[flag])+'l'
            
        if (i=='Trumpet' ):
            pattern=pattern+'T'+str(Detected_Notes[flag][0])+str(Onsets[flag])+'l'
                       
        flag+=1

    pattern=pattern+'p'
    ser.port='COM3'
    ser.open()
    ser.write(pattern)          #write to the port 