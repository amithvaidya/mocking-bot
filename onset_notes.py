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
#from feature_helper import estimated_f0, harmonics
#from utils import stft, plot_spectrum, plot_time_domain,read_all_wavedata,plot_feature
import wave
import struct

import numpy as np
import os




def onset_notes(file_name):

        #=======================================================================DEFINING FINAL DF TO WRITE TO CSV=====================================================================================
        columns1=['spectralCentroid_mean','spectralCentroid_std','spectralSpread_mean','spectralSpread_std','spectralFlux_mean','spectralFlux_std','spectralIrregularity_mean','spectralIrregularity_std','spectralFlatness_mean','spectralFlatness_std','zeroCrossingRate_mean','zeroCrossingRate_std','rootMeanSquare_mean','rootMeanSquare_std','mfcc1_mean','mfcc2_mean','mfcc3_mean','mfcc4_mean','mfcc5_mean','mfcc6_mean','mfcc7_mean','mfcc8_mean','mfcc9_mean','mfcc10_mean','mfcc11_mean','mfcc12_mean','mfcc13_mean','mfcc1_std','mfcc2_std','mfcc3_std','mfcc4_std','mfcc5_std','mfcc6_std','mfcc7_std','mfcc8_std','mfcc9_std','mfcc10_std','mfcc11_std','mfcc12_std','mfcc13_std','harmonicCentroid','harmonicDeviation','harmonicSpead','logAttackTime','temporalCentroid']
        final_df = DataFrame(columns= ['spectralCentroid_mean','spectralCentroid_std','spectralSpread_mean','spectralSpread_std','spectralFlux_mean','spectralFlux_std','spectralIrregularity_mean','spectralIrregularity_std','spectralFlatness_mean','spectralFlatness_std','zeroCrossingRate_mean','zeroCrossingRate_std','rootMeanSquare_mean','rootMeanSquare_std','mfcc1_mean','mfcc2_mean','mfcc3_mean','mfcc4_mean','mfcc5_mean','mfcc6_mean','mfcc7_mean','mfcc8_mean','mfcc9_mean','mfcc10_mean','mfcc11_mean','mfcc12_mean','mfcc13_mean','mfcc1_std','mfcc2_std','mfcc3_std','mfcc4_std','mfcc5_std','mfcc6_std','mfcc7_std','mfcc8_std','mfcc9_std','mfcc10_std','mfcc11_std','mfcc12_std','mfcc13_std','harmonicCentroid','harmonicDeviation','harmonicSpead','logAttackTime','temporalCentroid'])

        #=======================================================================AUDIO READ=========================================================================================
        #yyy--------------------------------------------------------------------------------------------------------------------------------------------------
        filename1=file_name
        sound_file = wave.open(filename1, 'rb')
                             
        #yyy--------------------------------------------------------------------------------------------------------------------------------------------------
        #=========================================================================ONSETS+CSVWRITE===========================================================================================

        #////////////////////--------------------------//////////////
        Onsets = []
        offsets=[]
        Detected_Notes=[]
        #////////////////----------------------//////////////////

        
        file_length = sound_file.getnframes()
        sound = np.zeros(file_length)

        for i in range(file_length):
                data = sound_file.readframes(1)
                data = struct.unpack("<h", data)
                sound[i] = int(data[0])
        sound = np.divide(sound, float(2**15))

        arr2=np.concatenate((np.zeros(1,dtype=int),np.ones(99,dtype=int)),axis=0)
        soundk=abs(sound)
        sound1=np.square(soundk)
        wtime=float(1000/44100.0)
        newa1=np.convolve(sound1,arr2,mode='full')
        newa3=10*np.log10(newa1+0.001)
        leng=len(newa3)
        windows=int(200)
        leng=int(len(newa3))
        yaya=np.zeros(int(leng/windows))
        for i in range(len(yaya)):
                okay=[(newa3[(i*200):((i+1)*200)])]
                yaya[i]=np.min(okay)

        yayak=np.zeros(int(len(yaya)/5))
        windowtime=[]
        
        for i in range(len(yayak)):
               
                  okay=[(yaya[(i*5):((i+1)*5)])]
                  yayak[i]=np.min(okay)
                  windowtime.append(i*wtime)
        

        #################### detecting onsets and silence parts #####################################################################################################################################3

        y=0
        c=0                                                                 #index to store onset
        #onset=np.zeros(int((file_length/1000)))                                       #onset array
        onset=list()
        onsetsize=0 
        yayak[0]=-30
        yayak[len(yayak)-1]=-30

        plt.plot(yayak)
        plt.show()

        am_max=-1*np.max(yayak)
        am_min=-1*np.min(yayak)
        err=am_min-am_max
        err1=err*0.4
        am_max1=am_max+err1
        midleveldb=-1*am_max1
        #////////////////------------------------//////////
        Onset=list()
        detect=list()
        
        #//////////////////---------------------///////
        
        flag1=0
        so=0
        yayak[len(yayak)-1]=-30               #first and last sample of yayak is made -30 db
        yayak[0]=-30
        done=0
        startz=0 
        endz=0      
        for i in range(0,len(yayak)-1,1):
                if(yayak[i]<=-27.7 and yayak[i+1]>-27.7):
                        startz=i
                        flag1=0
                if(yayak[i]>=-15):
                        flag1=1
                if(yayak[i]>=-27.7 and yayak[i+1]<-27.7):
                        endz=i
                        if(flag1==1):
                                onsetsize=onsetsize+1
                                onset.append(startz)
                                onset.append(endz)
                                c=c+1
                                flag1=0
                                print c

        print(onset)
                                

        spectralCentroid_mean=np.zeros(onsetsize)
        spectralCentroid_std=np.zeros(onsetsize)
        spectralSpread_mean=np.zeros(onsetsize)
        spectralSpread_std=np.zeros(onsetsize)
        spectralFlux_mean=np.zeros(onsetsize)
        spectralFlux_std=np.zeros(onsetsize)
        spectralIrregularity_mean=np.zeros(onsetsize)
        spectralIrregularity_std=np.zeros(onsetsize)
        spectralFlatness_mean=np.zeros(onsetsize)
        spectralFlatness_std=np.zeros(onsetsize)
        zeroCrossingRate_mean=np.zeros(onsetsize)
        zeroCrossingRate_std=np.zeros(onsetsize)
        rootMeanSquare_mean=np.zeros(onsetsize)
        rootMeanSquare_std=np.zeros(onsetsize)
        mfcc1_mean=np.zeros(onsetsize)
        mfcc2_mean=np.zeros(onsetsize)
        mfcc3_mean=np.zeros(onsetsize)
        mfcc4_mean=np.zeros(onsetsize)
        mfcc5_mean=np.zeros(onsetsize)
        mfcc6_mean=np.zeros(onsetsize)
        mfcc7_mean=np.zeros(onsetsize)
        mfcc8_mean=np.zeros(onsetsize)
        mfcc9_mean=np.zeros(onsetsize)
        mfcc10_mean=np.zeros(onsetsize)
        mfcc11_mean=np.zeros(onsetsize)
        mfcc12_mean=np.zeros(onsetsize)
        mfcc13_mean=np.zeros(onsetsize)
        mfcc1_std=np.zeros(onsetsize)
        mfcc2_std=np.zeros(onsetsize)
        mfcc3_std=np.zeros(onsetsize)
        mfcc4_std=np.zeros(onsetsize)
        mfcc5_std=np.zeros(onsetsize)
        mfcc6_std=np.zeros(onsetsize)
        mfcc7_std=np.zeros(onsetsize)
        mfcc8_std=np.zeros(onsetsize)
        mfcc9_std=np.zeros(onsetsize)
        mfcc10_std=np.zeros(onsetsize)
        mfcc11_std=np.zeros(onsetsize)
        mfcc12_std=np.zeros(onsetsize)
        mfcc13_std=np.zeros(onsetsize)
        harmonicCentroid=np.zeros(onsetsize)
        harmonicDeviation=np.zeros(onsetsize)
        harmonicSpead=np.zeros(onsetsize)
        logAttackTime=np.zeros(onsetsize)
        temporalCentroid=np.zeros(onsetsize)

        a=0 # stores the corresponding window it time frame 
        y=[] # list of onsets 
        z=[] # list of offset 

        k=0
        
        for i in range(onsetsize):
                a=round((onset[2*i]*wtime),2)
                y.append(a)
                a=round((onset[2*i+1]*wtime),2)
                z.append(a)
                
                features=Feature_value(sound[int(onset[2*i]*1000):int(onset[2*i+1]*1000)])    #<=========================================================================features
                note=(freqFind(sound[int(onset[2*i]*1000):int(onset[2*i+1]*1000)]))        #<=========================================================================detect+freqfind
                if(note==''):
                     note=freqFind(sound[int(onset[2*i]*1000):int((onset[2*i+1]*1000)+(onset[2*i]*1000))/2])
                     if(note==''):
                         note='A4'
                detect.append(note)
                print(detect)
                spectralCentroid_mean[i]=features[0]
                spectralCentroid_std[i]=features[1]
                spectralSpread_mean[i]=features[2]
                spectralSpread_std[i]=features[3]
                spectralFlux_mean[i]=features[4]
                spectralFlux_std[i]=features[5]
                spectralIrregularity_mean[i]=features[6]
                spectralIrregularity_std[i]=features[7]
                spectralFlatness_mean[i]=features[8]
                spectralFlatness_std[i]=features[9]
                zeroCrossingRate_mean[i]=features[10]
                zeroCrossingRate_std[i]=features[11]
                rootMeanSquare_mean[i]=features[12]
                rootMeanSquare_std[i]=features[13]
                mfcc1_mean[i]=features[14]
                mfcc2_mean[i]=features[15]
                mfcc3_mean[i]=features[16]
                mfcc4_mean[i]=features[17]
                mfcc5_mean[i]=features[18]
                mfcc6_mean[i]=features[19]
                mfcc7_mean[i]=features[20]
                mfcc8_mean[i]=features[21]
                mfcc9_mean[i]=features[22]
                mfcc10_mean[i]=features[23]
                mfcc11_mean[i]=features[24]
                mfcc12_mean[i]=features[25]
                mfcc13_mean[i]=features[26]
                mfcc1_std[i]=features[27]
                mfcc2_std[i]=features[28]
                mfcc3_std[i]=features[29]
                mfcc4_std[i]=features[30]
                mfcc5_std[i]=features[31]
                mfcc6_std[i]=features[32]
                mfcc7_std[i]=features[33]
                mfcc8_std[i]=features[34]
                mfcc9_std[i]=features[35]
                mfcc10_std[i]=features[36]
                mfcc11_std[i]=features[37]
                mfcc12_std[i]=features[38]
                mfcc13_std[i]=features[39]
                harmonicCentroid[i]=features[40]
                harmonicDeviation[i]=features[41]
                harmonicSpead[i]=features[42]
                logAttackTime[i]=features[43]
                temporalCentroid[i]=features[44]

                k=k+1

         #//////////////////---------------------///////
        Detected_Notes=detect[:k]
        Onsets=y[:k]
        offsets=z[:k]

        #print(Detected_Notes)
        #print(Onsets)
        #print(offsets)
        #print(Detected_Notes)

        #=======================================================================================================================================================================

        datasamp = {     'spectralCentroid_mean':spectralCentroid_mean,
                         'spectralCentroid_std':spectralCentroid_std,
                         'spectralSpread_mean':spectralSpread_mean,
                         'spectralSpread_std':spectralSpread_std,
                         'spectralFlux_mean':spectralFlux_mean,
                         'spectralFlux_std':spectralFlux_std,
                         'spectralIrregularity_mean':spectralIrregularity_mean,
                         'spectralIrregularity_std':spectralIrregularity_std,
                         'spectralFlatness_mean':spectralFlatness_mean,
                         'spectralFlatness_std':spectralFlatness_std,
                         'zeroCrossingRate_mean':zeroCrossingRate_mean,
                         'zeroCrossingRate_std':zeroCrossingRate_std,
                         'rootMeanSquare_mean':rootMeanSquare_mean,
                         'rootMeanSquare_std':rootMeanSquare_std,
                         'mfcc1_mean':mfcc1_mean,
                         'mfcc2_mean':mfcc2_mean,
                         'mfcc3_mean':mfcc3_mean,
                         'mfcc4_mean':mfcc4_mean,
                         'mfcc5_mean':mfcc5_mean,
                         'mfcc6_mean':mfcc6_mean,
                         'mfcc7_mean':mfcc7_mean,
                         'mfcc8_mean':mfcc8_mean,
                         'mfcc9_mean':mfcc9_mean,
                         'mfcc10_mean':mfcc10_mean,
                         'mfcc11_mean':mfcc11_mean,
                         'mfcc12_mean':mfcc12_mean,
                         'mfcc13_mean':mfcc13_mean,
                         'mfcc1_std':mfcc1_std,
                         'mfcc2_std':mfcc2_std,
                         'mfcc3_std':mfcc3_std,
                         'mfcc4_std':mfcc4_std,
                         'mfcc5_std':mfcc5_std,
                         'mfcc6_std':mfcc6_std,
                         'mfcc7_std':mfcc7_std,
                         'mfcc8_std':mfcc8_std,
                         'mfcc9_std':mfcc9_std,
                         'mfcc10_std':mfcc10_std,
                         'mfcc11_std':mfcc11_std,
                         'mfcc12_std':mfcc12_std,
                         'mfcc13_std':mfcc13_std,
                         'harmonicCentroid':harmonicCentroid,
                         'harmonicDeviation':harmonicDeviation,
                         'harmonicSpead':harmonicSpead,
                         'logAttackTime':logAttackTime,
                         'temporalCentroid':temporalCentroid
                          
              }

        er=DataFrame(datasamp,columns=columns1)
        final_df=pd.concat([final_df,er])
        data_csv_name='TESTFORML_sat_practise_AUDIO.csv'
        
        pd.options.mode.use_inf_as_na = True
        final_df=final_df.fillna(0)
        final_df.to_csv ((path+'\\'+data_csv_name+'.csv'), index = None, header=True) #Don't forget to add '.csv' at the end of the path      

        #HOLY GRAIL
        return (Detected_Notes,Onsets)
        

