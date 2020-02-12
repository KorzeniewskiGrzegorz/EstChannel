% white noise in pulses generator

close all
clear all
Fs = 38e6;  % sample freq [Hz]
R=0.1; % pulse ratio (0-1 range) for signal break
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

QData = zeros(1,data_len);

t = 0:1/Fs:(data_len-1)/Fs;

%windows
figure
plot(t(Fs*0.6:Fs*0.7) , IData(Fs*0.6:Fs*0.7))
xlabel("Time [s]")
ylabel("Norm. magnitude [AU]")

%syncpulse
figure
plot(t(Fs*0.45:Fs*0.65) , IData(Fs*0.45:Fs*0.65))
xlabel("Time [s]")
ylabel("Norm. magnitude [AU]")
xlim([0.45 0.65])


%%% SET FONT 30