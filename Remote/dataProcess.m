% data proccessing for white noise

close all
clear all
format long

%%%%%%%%%%%%%%%%%%%%%%%


Fs=20e6; %Sample freq
R=0.99; % ratio, the same as in generator script
signalDuration = 1;% calibration time [s] , corresponds to parameters of signal generation
offman=0;
wd=10; % window duration [us] for the correlation purpose


connectionType="cable";
savePath="/home/udg/Dropbox/UDG/magisterka/pomiary/";

%path="/tmp/";
path="/dev/shm/";
%path="/home/udg/Escritorio/datos/";

%%%%%%%%%5%%%%%%%%%%%%%
fid=fopen(path+"ruidoR.dat",'rb');
ruidoR=fread(fid,'float');

fid=fopen(path+"ruidoI.dat",'rb');
ruidoI=fread(fid,'float');

ruidoC=complex(ruidoR,ruidoI);  %transmitted complex data

clear ruidoR
clear ruidoI

lenRRaw=size(ruidoC(:,1));
lenRRaw=lenRRaw(1,1);


fid=fopen(path+"dataR.dat",'rb');
dataR=fread(fid,'float');

fid=fopen(path+"dataI.dat",'rb');
dataI=fread(fid,'float');
%lenDIRaw=size(dataI(:,1));
%lenDIRaw=lenDIRaw(1,1);

%dataR=dataR(1:lenDIRaw);
dataC=complex(dataR,dataI); % received complex data
%probka=dataR;
clear dataR
clear dataI

lenDRaw=size(dataC(:,1));
lenDRaw=lenDRaw(1,1);



%Raw data plotting

%figure
%subplot(2,1,1)
%plot(0:1/Fs:2.5-1/Fs,real(ruidoC(1:2.5*Fs)),0:1/Fs:2.5-1/Fs,imag(ruidoC(1:2.5*Fs)))
%title('Tx Raw Data')
%xlabel('time [s]')
%subplot(2,1,2)
%plot(0:1/Fs:2.5-1/Fs,real(dataC(1:2.5*Fs)),0:1/Fs:2.5-1/Fs,imag(dataC(1:2.5*Fs)))
%title('Rx Raw Data')
%xlabel('time [s]')

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Calibration processing


F=1/signalDuration ; 
calibrationOffset = signalDuration *Fs ; % conversion from time to samples


% signal calibration
offset =(-1) *(offsetcalc(abs(dataC),Fs,0.004,0.5))-offman ; % received samples offset due to hardware & software lag [samples] -117106;


dataC=dataC(calibrationOffset+offset+1:calibrationOffset*2+offset-(Fs/F)*(1-R)+2);
ruidoC=ruidoC(calibrationOffset:calibrationOffset*2 -(Fs/F)*(1-R)+1);

lenR=size(ruidoC(:,1));
lenR=lenR(1,1);

lenD=size(dataC(:,1));
lenD=lenD(1,1);


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

for i=0: v-1% Run cross correlation for v times
    

    x=ruidoC(i*N+1:i*N+N,1); % TX
    y=dataC(i*N+1:i*N+N,1); % RX
    
    rxy=xcorr(x,conj(y)); % Cross correlation of the TX and RX conjugated data
    Ryx=flip(rxy(1:N)); % Flip the correlation result and take the first N samples (Ryx(t) = Rxy(-t)
    
    

PA(:,i+1)=Ryx'; %Store the results in an array
end
clear Ryx; 
 
Ryx=sum(PA')/v; % Average the values 



figure;
plot(0:1/Fs*1000000:N/Fs*1000000-1/Fs*1000000,abs(Ryx)); % Plot the estimated impulse response
title('Estimated Impulse Response');
xlabel('time [us]')
grid;

%%%%%%%%%%%% GUARDAR RESPUESTA AL IMPULSO %%%%%%%%%%%%%%%%%

%guardarRespAlImpulso(abs(Ryx),savePath,Fs,wd,connectionType);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



%[maximum,pico]=max(abs(Ryx));
%pico=pico/Fs

%f = fopen ("datos/ImpResp.dat", 'ab');
%v = fwrite (f, abs(Ryx),'float');
%fclose (f);

%&&&&&&&&&&&&&&&&&&&&&&


%modu= conv(ruidoC,Ryx);

%lenM=size(modu(:,1));
%lenM=lenM(1,1);
%figure
%plot(0:1/Fs:lenM/Fs-1/Fs,real(modu),0:1/Fs:lenM/Fs-1/Fs,imag(modu))


