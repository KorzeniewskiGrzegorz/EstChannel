% data proccessing for white noise

close all
clear all
format long

%%%%%%%%%%%%%%%%%%%%%%%


Fs=20e6; %Sample freq

path="/dev/shm/";


%%%%%%%%%5%%%%%%%%%%%%%
%fid=fopen(path+"ruidoR.dat",'rb');
%dataR=fread(fid,'float');

%fid=fopen(path+"ruidoI.dat",'rb');
%dataI=fread(fid,'float');

fid=fopen(path+"fdataR.dat",'rb');
dataR=fread(fid,'float');

fid=fopen(path+"fdataI.dat",'rb');
dataI=fread(fid,'float');





lenDRaw=length(dataR(:,1));

dataC=complex(dataR,dataI); 

%Raw data plotting

figure

plot(abs(dataC))%,0:1/Fs:lenDRaw/Fs-1/Fs,dataI)
title('Rx Raw Data')
xlabel('time [s]')


%X=fftshift(fft(dataR+dataI));
%N=length(X);
%figure;
%plot(Fs*(-N/2:N/2-1)/N,abs(X));
%grid on;
