

% white noise in pulses generator

close all
clear all
Fs=20e6;  % sample freq [Hz]
R=0.99; % pulse ratio (0-1 range) for signal break
segundos=1; % signal duration [s]
%path="/tmp/";
path="/dev/shm/";
%path="/home/udg/Escritorio/datos/";

IData = zeros(1,Fs*segundos);

IData(1,1:Fs*segundos- Fs*segundos*(1-R)) = randn(1,Fs*segundos- Fs*segundos*(1-R)); %First cycle



data_len = size(IData);
data_len = data_len(2);

%QData = [zeros(1,Fs/4) IData]; % 90 degree delay, quadrature signal
%QData = QData(1,1:data_len);

QData = zeros(1,data_len);


t = 0:1/Fs:segundos-1/Fs;

plot(t,IData,'b',t,QData,'r')

f = fopen (path+"IPulse.dat", 'wb');
v = fwrite (f, IData,'float');
fclose (f);

f = fopen (path+"QPulse.dat", 'wb');
v = fwrite (f, QData,'float');
fclose (f);

