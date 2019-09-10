% data proccessing for white noise

close all
clear all
format long

%%%%%%%%%%%%%%%%%%%%%%%


Fs=35e6; %Sample freq

path="/dev/shm/";


%%%%%%%%%5%%%%%%%%%%%%%
%fid=fopen(path+"ruidoR.dat",'rb');
%ruidoR=fread(fid,'float');

%fid=fopen(path+"ruidoI.dat",'rb');
%ruidoI=fread(fid,'float');

fid=fopen(path+"dataR.dat",'rb');
dataR=fread(fid,'float');

fid=fopen(path+"dataI.dat",'rb');
dataI=fread(fid,'float');

%dataR = dataR(1:2*Fs);
%dataI = dataI(1:2*Fs);


%lenRRaw=length(ruidoR(:,1));

lenDRaw=length(dataR(:,1));

%ruidoC=complex(ruidoR,ruidoI); 
dataC=complex(dataR,dataI); 

%clear ruidoR
%clear ruidoI
clear dataR
clear dataI
%Raw data plotting

%figure

%plot(0:1/Fs:lenRRaw/Fs-1/Fs,abs(ruidoC))%,0:1/Fs:lenDRaw/Fs-1/Fs,dataI)
%title('Rx Raw Data')
%xlabel('time [s]')


figure

plot(0:1/Fs:lenDRaw/Fs-1/Fs,abs(dataC))%,0:1/Fs:lenDRaw/Fs-1/Fs,dataI)
title('Rx Raw Data')
xlabel('time [s]')


%X=fftshift(fft(dataR+dataI));
%N=length(X);
%figure;
%plot(Fs*(-N/2:N/2-1)/N,abs(X));
%grid on;
