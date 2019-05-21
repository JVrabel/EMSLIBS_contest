%clear all;

cd 'f:\DATA\EMSLIBS_CONTEST\';

h5disp('contest_TRAIN.h5')
trainData = h5read('contest_TRAIN.h5','/Spectra/001');
wavelengths = h5read('contest_TRAIN.h5','/Wavelengths/1');
trainClass = h5read('contest_TRAIN.h5','/Class/1');

spectraCount = 100;
trainData = trainData(1:spectraCount,:);

for i = 1:(100-1)
sequence = [2:100];
temp_trainData = h5read('contest_TRAIN.h5',sprintf('/Spectra/%03d',sequence(i)));
temp_trainData = temp_trainData(1:spectraCount,:);
trainData = cat(1,trainData,temp_trainData);
end

redClass = trainClass(1:spectraCount);
for i = [500:500:49500]
  tempClass = trainClass((i+1):(i+spectraCount));
  redClass = cat(1,redClass,tempClass); 
end
trainClass = redClass;
testData = h5read('contest_TEST.h5','/UNKNOWN/1');
temp_testData = h5read('contest_TEST.h5','/UNKNOWN/2');
testData = cat(1,testData,temp_testData);

clearvars -except trainData testData wavelengths trainClass
