## install libraries for import
try:
    from pip import main as pipmain
except ImportError:
    from pip._internal import main as pipmain

pipmain(["install", 'h5py'])
pipmain(["install", 'numpy'])

## import libraries
import os
import h5py
import numpy as np

## set number of spectra and path to the data files
os.chdir("f:/Data/EMSLIBS_CONTEST/")   # selecting the directory containing the data files
spectraCount = 200                           # selecting the number of spectra for each sample (maximum of 500)

##########################################
# Train Data
##########################################

trainFile = h5py.File("contest_TRAIN.h5",'r')   # training data, unless the filename was changed

wavelengths = trainFile["Wavelengths"]
wavelengths = wavelengths[list(wavelengths.keys())[0]].value
# creates a one-dimensional array (vector) containing the wavelengths

for sample in list(trainFile["Spectra"].keys()):
    tempData = trainFile["Spectra"][sample].value
    tempData = tempData[:,0:spectraCount]
    if "trainData" not in locals():
        trainData = tempData.transpose()
    else:
        trainData = np.append(trainData, tempData.transpose(), axis = 0)
# creates a two-dimensional array (matrix) containing the training data
# each row represents a single spectrum

trainClass = trainFile["Class"]["1"].value
for i in range(0,50000,500):
    if i == 0:
        tempClass = trainClass[0:spectraCount]
    else:
        tempClass = np.append(tempClass, trainClass[i:(i+spectraCount)])
trainClass = tempClass
# creates a one-dimensional array (vector) containing the classes corresponding to the spectra in the training dataset
# the order of the classes is the same as the order of the spectra
# if the dataset is reordered (e.g., randomly sampled), make sure that the classes are reordered accordingly
trainFile.close()
del tempClass, tempData, i, sample

##########################################
# Test Data
##########################################

testFile = h5py.File("contest_TEST.h5",'r')     # testing data, unless the filename was changed

for sample in list(testFile["UNKNOWN"].keys()):
    tempData = testFile["UNKNOWN"][sample].value
   
    if "testData" not in locals():
        testData = tempData.transpose()
    else:
       testData = np.append(testData, tempData.transpose(), axis = 0)


# creates a two-dimensional array (matrix) containing the testing data
# each row represents a single spectrum
testFile.close()
del tempData, sample, spectraCount

##########################################
# End of loading script
##########################################
# Returns 4 variables -> trainData, trainClass, testData, wavelengths
##########################################