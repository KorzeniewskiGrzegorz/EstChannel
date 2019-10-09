

% white noise in pulses generator

close all
clear all
Fs = 38e6;  % sample freq [Hz]
R=0.01; % pulse ratio (0-1 range) for signal break
duration=1;% signal duration [s]
wd=0.0001; % window duration [s]
path="/dev/shm/";





IData = zeros(1,floor(Fs*duration));

v = duration/wd;
N= Fs*wd ;


for i=1: v
    w = zeros(1,floor(Fs*wd));
    w(1,1:floor(Fs*wd)- floor(Fs*wd)*(1-R)) = randn(1,floor(Fs*wd)- floor(Fs*wd)*(1-R));


    IData(1,(i-1)*N+1:i*N) = w; 
end

IData = IData/ max(IData);

ISync = syncpulse(Fs,0.6);

IData = [ISync, IData];



data_len =length(IData);

%QData = [zeros(1,Fs/4) IData]; % 90 degree delay, quadrature signal
%QData = QData(1,1:data_len);

QData = zeros(1,data_len);



t = 0:1/Fs:(data_len-1)/Fs;

figure
plot(t,IData,'b',t,QData,'r')

f = fopen (path+"IPulse.dat", 'wb');
fwrite (f, IData,'float');
fclose (f);

f = fopen (path+"QPulse.dat", 'wb');
fwrite (f, QData,'float');
fclose (f);

