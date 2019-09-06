% Quadratic pulse generator

close all
clear all
Fs=5e6;  % sample freq [Hz]
F=1; % pulse frequency [Hz]
R=0.2; % pulse ratio (0-1 range)
segundos=1; % signal duration [s]

path="/home/udg/Dropbox/UDG/shddata/";

IData = zeros(1,Fs*segundos);

IData(1,1:Fs/F*R) = 1; %First cycle

for i=1: segundos*F-1/Fs
  
    IData(1,i*Fs/F+1:i*Fs/F+R*Fs/F)=1;
end

data_len = size(IData);
data_len = data_len(2);

%QData = [zeros(1,Fs/F/4) IData]; % 90 degree delay, quadrature signal
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

