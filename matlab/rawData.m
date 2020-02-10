% data proccessing for white noise


clear all
format long

%%%%%%%%%%%%%%%%%%%%%%%


Fs=38e6; %Sample freq

path="/dev/shm/";



%%%%%%%%%5%%%%%%%%%%%%%
fid=fopen(path+"ruidoR.dat",'rb');
ruidoR=fread(fid,'float');

fid=fopen(path+"ruidoI.dat",'rb');
ruidoI=fread(fid,'float');

%fid=fopen(path+"fdataR.dat",'rb');
%bdataR=fread(fid,'float');

%fid=fopen(path+"fdataI.dat",'rb');
%bdataI=fread(fid,'float');

%bdataR = bdataR(1:2*Fs);
%bdataI = bdataI(1:2*Fs);

lenDRaw=length(ruidoR(:,1));

ruidoC=complex(ruidoR,ruidoI); 
%bdataC=complex(bdataR,bdataI); 


%y = doFilterLow(dataC);

%clear ruidoR
%clear ruidoI
%clear dataR
%clear dataI
%Raw data plotting

figure

plot(0:1/Fs:lenDRaw/Fs-1/Fs,real(ruidoC)+ imag(ruidoC))%,0:1/Fs:lenDRaw/Fs-1/Fs,dataI)
title('bad')
xlabel('time [s]')

offset = 0.57*Fs;
snr = SNRcalc(bdataC (1:0.6*Fs),Fs,offset);

%path="/home/udg/Documentos/8dbsnr/";



%fid=fopen(path+"fdataR.dat",'rb');
%dataR=fread(fid,'float');
%
%fid=fopen(path+"fdataI.dat",'rb');
%dataI=fread(fid,'float');

%dataR = dataR(1:0.6*Fs);
%dataI = dataI(1:0.6*Fs);


%lenRRaw=length(ruidoR(:,1));

%l%enDRaw=length(dataR(:,1));

%ruidoC=complex(ruidoR,ruidoI); 
%dataC=complex(dataR,dataI); 


%y = doFilterLow(dataC);

%clear ruidoR
%clear ruidoI
%clear dataR
%clear dataI
%Raw data plotting

%figure

%plot(0:1/Fs:lenDRaw/Fs-1/Fs,real(dataC)+ imag(dataC))%,0:1/Fs:lenDRaw/Fs-1/Fs,dataI)
%title('good')
%xlabel('time [s]')


%figure

%plot(0:1/Fs:lenDRaw/Fs-1/Fs,real(y)+ imag(y))%;,0:1/Fs:lenDRaw/Fs-1/Fs,imag(dataC))%,0:1/Fs:lenDRaw/Fs-1/Fs,dataI)
%grid on
%title('filtered')
%xlabel('time [s]')


%X=fftshift(fft(real(dataC)+imag(dataC)));
%N=length(X);
%figure;
%plot(Fs*(-N/2:N/2-1)/N,abs(X));
%grid on;

%f = fopen (path+"filsyncdataR.dat", 'wb');
%fwrite (f, real(y),'float');
%fclose (f);

%f = fopen (path+"filsyncdataR.dat", 'wb');
%fwrite (f,imag(y),'float');
%fclose (f);
