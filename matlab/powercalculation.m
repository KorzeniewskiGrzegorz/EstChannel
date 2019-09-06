% data proccessing for white noise

close all
clear all
format long

%%%%%%%%%%%%%%%%%%%%%%%


Fs=20e6; %Sample freq

path="/dev/shm/";


%%%%%%%%%5%%%%%%%%%%%%%
fid=fopen(path+"ruidoR.dat",'rb');
ruidoR=fread(fid,'float');

fid=fopen(path+"ruidoI.dat",'rb');
ruidoI=fread(fid,'float');

fid=fopen(path+"dataR.dat",'rb');
dataR=fread(fid,'float');

fid=fopen(path+"dataI.dat",'rb');
dataI=fread(fid,'float');



lenRRaw=length(ruidoR(:,1));

lenDRaw=length(dataR(:,1));

ruidoC=complex(ruidoR,ruidoI); 
dataC=complex(dataR,dataI); 

clear ruidoR
clear ruidoI
clear dataR
clear dataI
%Raw data plotting

figure

plot(0:1/Fs:lenRRaw/Fs-1/Fs,abs(ruidoC))%,0:1/Fs:lenDRaw/Fs-1/Fs,dataI)
title('Rx Raw Data')
xlabel('time [s]')


figure

plot(abs(dataC))%,0:1/Fs:lenDRaw/Fs-1/Fs,dataI)
title('Rx Raw Data')
xlabel('time [s]')


sync = abs(dataC);
signal = sync(floor((0.1+0.02)*Fs):floor((0.1+0.04)*Fs));

%figure
%plot(signal)

noise = sync(floor((0.1-0.04)*Fs):floor((0.1-0.02)*Fs));

%figure
%plot(noise)

meanSignal = mean(signal);

meanNoise = mean(noise);
Ratio = meanSignal/meanNoise;

threshold = meanNoise +0.2*Ratio*meanNoise;
offset = floor(find(sync > threshold,1) +0.1*Fs ) -15

figure
plot(sync(offset:offset+Fs*0.99))
