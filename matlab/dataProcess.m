% data proccessing for white noise

close all
clear all
format long

%%%%%%%%%%%%%%%%%%%%%%%


Fs=20e6; %Sample freq
wd=100; % window duration [us] for the correlation purpose
path="/dev/shm/";


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

dataC=complex(dataR,dataI); % received complex data

clear dataR
clear dataI

lenDRaw=size(dataC(:,1));
lenDRaw=lenDRaw(1,1);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Calibration processing



calibrationOffset = 0.2 *Fs ; % conversion from time to samples


% signal calibration
offset = offsetcalc(dataC,Fs); % received samples offset due to hardware & software lag [samples]


fid=fopen(path+"fdataR.dat",'rb');
dataR=fread(fid,'float');

fid=fopen(path+"fdataI.dat",'rb');
dataI=fread(fid,'float');

dataC=complex(dataR,dataI); % filtered rx complex data

dataC  = dataC (offset+1:offset +Fs);
ruidoC = ruidoC(calibrationOffset+1:calibrationOffset+Fs);

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
    

    x=ruidoC(i*N+1:i*N+N,1); % TX
    y=dataC(i*N+1:i*N+N,1); % RX
    
    rxy=xcorr(x,conj(y)); % Cross correlation of the TX and RX conjugated data
    Ryx=flip(rxy(1:N)); % Flip the correlation result and take the first N samples (Ryx(t) = Rxy(-t)
    %hold on
    %figure
    %plot(x)
    %plot(abs(y))
    %hold off
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


