

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
    w(1,1) = randn;


    IData(1,(i-1)*N+1:i*N) = w; 
end

IData = IData/ max(IData);

ISync = syncpulse(Fs,0.6);

IData = [ISync, IData];

%status = save_sc16q11("/dev/shm/sin.sc16q11",ISync)

data_len =length(IData);

QData = zeros(1,data_len);



t = 0:1/Fs:(data_len-1)/Fs;

figure
plot(t,IData,'b',t,QData,'r')


CData= complex(IData,QData);

status = save_sc16q11("/dev/shm/tx.bin",CData)


IData = [IData,IData];
data_len =length(IData);

QData = zeros(1,data_len);

f = fopen (path+"ruidoR.dat", 'wb');
fwrite (f, IData,'float');
fclose (f);

f = fopen (path+"ruidoI.dat", 'wb');
fwrite (f, QData,'float');
fclose (f);
