# -*- coding: utf-8 -*-
#%%
import h5py
import os
import numpy as np
#%%
spectraCount = 100 #selecting the number of spectra for each sample (maximum of 500)
os.chdir("f:/DATA_JAKUB_V/emslibs_contest/EMSLIBS_CONTEST/") #selecting the directory containing the data files

testFile = h5py.File("contest_TEST.h5",'r') #testing data, unless the filename was changed
trainFile = h5py.File("contest_TRAIN.h5",'r') #training data, unless the filename was changed
#%%
wavelengths = testFile["Wavelengths"]
wavelengths = wavelengths[list(wavelengths.keys())[0]].value #creates a one-dimensional array (vector) containing the wavelengths

if "testData" in locals():
  del testData
for sample in list(testFile["UNKNOWN"].keys()):
  tempData = testFile["UNKNOWN"][sample].value
  tempData = tempData[:,0:spectraCount]
  if "testData" not in locals():
    testData = tempData.transpose()
  else:
    testData = np.append(testData, tempData.transpose(), axis = 0)
#creates a two-dimensional array (matrix) containing the testing data
#each row represents a single spectrum
    
    
testClass = testFile["Class"]["1"].value
for i in range(0,19000,500):
  if i == 0:
    test_tempClass = testClass[0:spectraCount]
  else:
    test_tempClass = np.append(test_tempClass, testClass[i:(i+spectraCount)])
testClass = test_tempClass
#creates a one-dimensional array (vector) containing the classes corresponding to the spectra in the training dataset
#the order of the classes is the same as the order of the spectra
#if the dataset is reordered (e.g., randomly sampled), make sure that the classes are reordered accordingly
testFile.close()

del tempData, sample, test_tempClass
#%%
if "trainData" in locals():
  del trainData
for sample in list(trainFile["Spectra"].keys()):
  tempData = trainFile["Spectra"][sample].value
  tempData = tempData[:,0:spectraCount]
  if "trainData" not in locals():
    trainData = tempData.transpose()
  else:
    trainData = np.append(trainData, tempData.transpose(), axis = 0)
#creates a two-dimensional array (matrix) containing the training data
#each row represents a single spectrum

trainClass = trainFile["Class"]["1"].value
for i in range(0,50000,500):
  if i == 0:
    tempClass = trainClass[0:spectraCount]
  else:
    tempClass = np.append(tempClass, trainClass[i:(i+spectraCount)])
trainClass = tempClass
#creates a one-dimensional array (vector) containing the classes corresponding to the spectra in the training dataset
#the order of the classes is the same as the order of the spectra
#if the dataset is reordered (e.g., randomly sampled), make sure that the classes are reordered accordingly
trainFile.close()

del tempClass, tempData, i, sample, spectraCount


