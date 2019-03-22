#rm (list=ls(all=TRUE))
#gc()
#install.packages("rhdf5")
library(rhdf5)


setwd("f:/DATA_JAKUB_V/emslibs_contest/EMSLIBS_CONTEST/")
wavelength <- as.data.frame(h5read(file = "contest_TRAIN.h5", name = "Wavelengths")) # import wavelengths
class <- as.data.frame(h5read(file = "contest_TRAIN.h5", name = "Class")) # import classes
spectra <- h5read(file = "contest_TRAIN.h5", name = "Spectra") # import spectra
h5closeAll()

##########################################
# Reduce number of spectra per sample
##########################################
N <- 100
reddim <- function(x){
  x <- x[1:N,]
}
spectra <- lapply(spectra,reddim)
##########################################

dataset <- as.data.frame(do.call('rbind',spectra))
spectraCount <- 100
trainClass = class
tempClass <- vector()
redClass <- class[(1):(spectraCount),]
for (i in c(seq(500,49500,500))){
  tempClass <- class[(i+1):(i+spectraCount),]
  redClass <-  append(redClass,tempClass)
  
  }
trainClass <- redClass

##########################################
# Test Data
##########################################

class_TEST <- as.data.frame(h5read(file = "contest_TEST.h5", name = "Class")) # import classes
spectra_TEST <- h5read(file = "contest_TEST.h5", name = "UNKNOWN") # import spectra
h5closeAll()

spectraCount <- 100
testClass = class_TEST
tempClass <- vector()
redTestClass <- class_TEST[(1):(spectraCount),]
for (i in c(seq(500,18500,500))){
  tempClass <- class_TEST[(i+1):(i+spectraCount),]
  redTestClass <-  append(redTestClass,tempClass)
  
}
testClass <- redTestClass

##########################################
# Reduce number of spectra per sample
##########################################
N <- 100
reddim <- function(x){
  x <- x[1:N,]
}
spectra_TEST <- lapply(spectra_TEST,reddim)
##########################################

dataset_TEST <- as.data.frame(do.call('rbind',spectra_TEST))

 
