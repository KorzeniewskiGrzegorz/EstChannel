% data proccessing for white noise

close all
clear all
format long

%%%%%%%%%%%%%%%%%%%%%%%


Fs=10e6; %Sample freq
wd=10; % window duration [us] for the correlation purpose
path="/dev/shm/";


%%%%%%%%%5%%%%%%%%%%%%%
fid=fopen(path+"ruidoR.dat",'rb');
ruidoR=fread(fid,'float');

fid=fopen(path+"ruidoI.dat",'rb');
ruidoI=fread(fid,'float');

ruidoR = ruidoR(1:2*Fs);
ruidoI = ruidoI(1:2*Fs);
ruidoC=complex(ruidoR,ruidoI);  %transmitted complex data

clear ruidoR
clear ruidoI

lenRRaw=length(ruidoC(:,1));

fid=fopen(path+"fdataR.dat",'rb');
dataR=fread(fid,'float');


fid=fopen(path+"fdataI.dat",'rb');
dataI=fread(fid,'float');

dataR = dataR(1:2*Fs);
dataI = dataI(1:2*Fs);
dataC=complex(dataR,dataI); % received complex data

clear dataR
clear dataI

lenDRaw=length(dataC(:,1));

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Calibration processing



calibrationOffset = 0.6 *Fs ; % conversion from time to samples



% signal calibration
offset =offsetcalc(dataC (1:0.6*Fs),Fs); % received samples offset due to hardware & software lag [samples]floor(0.447352158*Fs)

%snr = SNRcalc(dataC (1:0.6*Fs),Fs,offset);
dataC  = dataC (offset+1:offset +1*Fs);
ruidoC = ruidoC(calibrationOffset+1:calibrationOffset+1*Fs);

lenR=length(ruidoC(:,1));
lenD=length(dataC(:,1));

%calibrated data plotting

figure
subplot(2,1,1)
plot(0:1/Fs:lenR/Fs-1/Fs,real(ruidoC),0:1/Fs:lenR/Fs-1/Fs,imag(ruidoC))
title('Tx calibrated')
xlabel('time [s]')
subplot(2,1,2)
plot(0:1/Fs:lenD/Fs-1/Fs,real(dataC),0:1/Fs:lenD/Fs-1/Fs,imag(dataC))
title('Rx with offset')
xlabel('time [s]')


N=wd*Fs/1000000 ; % conversion of window duration from miliseconds to samples

v=floor(lenD/N); % number of pulses recorded

y=zeros(N,v);


for i=0:v-1 % Run cross correlation for v times
    
    y=dataC(i*N+1:i*N+N,1); % RX
    ryy= y*y';
    
    Ryy= ryy(:,1);
    
    
    
PA(:,i+1)=Ryy; %Store the results in an array
end
clear Ryx; 
 
ERyy=sum(PA')/v; % Average the values 

%ERyy = ERyy/ max(ERyy);
h = ERyy;



figure;
plot(0:1/Fs*1000000:N/Fs*1000000-1/Fs*1000000,abs(h)); % Plot the estimated impulse response

title('Estimated Impulse Response');
xlabel('time [us]')
grid;

%%%%%%%%%%%% GUARDAR RESPUESTA AL IMPULSO %%%%%%%%%%%%%%%%%

%guardarRespAlImpulso(abs(Ryx),savePath,Fs,wd,connectionType);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



%[maximum,pico]=max(abs(Ryx));
%pico=pico/Fs


%&&&&&&&&&&&&&&&&&&&&&&


%modu= conv(ruidoC,Ryx);

%lenM=size(modu(:,1));
%lenM=lenM(1,1);
%figure
%plot(0:1/Fs:lenM/Fs-1/Fs,real(modu),0:1/Fs:lenM/Fs-1/Fs,imag(modu))


