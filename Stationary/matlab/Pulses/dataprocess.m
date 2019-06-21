% data proccessing

close all
clear all
format long
Fs=100e3; %Sample freq

fid=fopen("datos/ruidoR.dat",'rb');
ruidoR=fread(fid,'float');

fid=fopen("datos/ruidoI.dat",'rb');
ruidoI=fread(fid,'float');

ruidoC=complex(ruidoR,ruidoI);  %transmitted data

fid=fopen("datos/dataR.dat",'rb');
dataR=fread(fid,'float');

fid=fopen("datos/dataI.dat",'rb');
dataI=fread(fid,'float');

dataC=complex(dataR,dataI); % received data

lenR=size(ruidoC(:,1));
lenR=lenR(1,1);

lenD=size(dataC(:,1));
lenD=lenD(1,1);

lenDr=size(dataR(:,1));
lenDr=lenDr(1,1);

figure
subplot(2,1,1)
plot(0:1/Fs:lenR/Fs-1/Fs,ruidoR,0:1/Fs:lenR/Fs-1/Fs,ruidoI)
title('Tx real part')
xlabel('time [s]')
subplot(2,1,2)
plot(0:1/Fs:lenDr/Fs-1/Fs,dataR,0:1/Fs:lenDr/Fs-1/Fs,dataI)
title('Rx real part')
xlabel('time [s]')

offset = 371397; % received samples offset

dataC=dataC(offset:lenD);

lenD=size(dataC(:,1));
lenD=lenD(1,1);


F=1000; % Pulse freq
N=Fs/F; % window duration [samples], should be the duration of a pulse  

v=floor(lenD/N); % number of pulses recorded






y=zeros(N,v);

for i=0: v-1% Run cross correlation for v times
    
   

    
   

    x=ruidoC(i*N+1:i*N+N,1); % TX
    y=dataC(i*N+1:i*N+N,1); % RX
    
    rxy=xcorr(x,conj(y)); % Cross correlation of the TX and RX conjugated data
    Ryx=flip(rxy(1:N)); % Flip the correlation result and take the first N samples (Ryx(t) = Rxy(-t)
   %Ryx=flip(rxy);

PA(:,i+1)=Ryx'; %Store the results in an array
end
clear Ryx; 
 
Ryx=sum(PA')/v; % Average the values 

%figure;
%plot(abs(Ryx))

figure;
plot(0:1/Fs:N/Fs-1/Fs,abs(Ryx)); % Plot the estimated impulse response
title('Estimated Impulse Response');
xlabel('time [s]')
grid;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
hold on
R=0.05;%ratio

Pulso = zeros(1,N);

Pulso(1,1:Fs/F*R) = 1; 
att=0.25;

plot(0:1/Fs:N/Fs-1/Fs,Pulso*att);

%QPulso = [zeros(1,Fs/F/4) Pulso]; % 90 degree delay, quadrature signal
%QPulso = QPulso(1,1:N);
%plot(0:1/Fs:N/Fs-1/Fs,QPulso*att);

hold off
%%%%%%%%%%%%%%%%%%%%5

[maximum,pico]=max(abs(Ryx));
pico=pico/Fs

f = fopen ("datos/ImpResp.dat", 'ab');
v = fwrite (f, abs(Ryx),'float');
fclose (f);