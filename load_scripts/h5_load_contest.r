# In case of missing library rhdf5, uncomment following line for first run of the script. Not needed later
# install.packages("rhdf5")
library(rhdf5)

# In case of insufficent memory, uncomment following line. Your disc will be used as buffer and data might be loaded
# memory.limit(size=65536)

# set number of spectra and path to the data files
setwd("D:/data/EMSLIBS contest/data/")    # selecting the directory containing the data files
spectraCount <- 100   # selecting the number of spectra for each sample (maximum of 500), recommended 100

##########################################
# Train Data
##########################################

wavelengths <- as.data.frame(h5read(file = "contest_TRAIN.h5", name = "Wavelengths")) # import wavelengths
trainClass <- as.data.frame(h5read(file = "contest_TRAIN.h5", name = "Class")) # import classes
trainData <- h5read(file = "contest_TRAIN.h5", name = "Spectra") # import spectra
h5closeAll()

##########################################
# Reduce number of spectra per sample
##########################################

reddim <- function(x){
  x <- x[1:spectraCount,]
}
trainData <- lapply(trainData,reddim)

##########################################

trainData <- as.data.frame(do.call('rbind',trainData))
tempClass <- vector()
redClass <- trainClass[(1):(spectraCount),]
for (i in c(seq(500,49500,500))){
  tempClass <- trainClass[(i+1):(i+spectraCount),]
  redClass <-  append(redClass,tempClass)
  
}
trainClass <- redClass

##########################################
# Test Data
##########################################

testData <- h5read(file = "contest_TEST.h5", name = "UNKNOWN") # import spectra
h5closeAll()

##########################################
# Reduce number of spectra per sample
##########################################

testData <- lapply(testData,reddim)
testData <- as.data.frame(do.call('rbind',testData))

##########################################

rm(i, redClass, spectraCount, tempClass, reddim)
gc()

##########################################
# End of loading script
##########################################