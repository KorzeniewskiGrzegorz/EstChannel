close all
clear all

path = "/home/udg/git/EstChannel/mediciones/biurkoFranka/agc on/";

Fs = 38e6
fid=fopen(path +"Fs38-Fr2170-bw28-wd10--1.dat",'rb');
imp=fread(fid,'double');

path = "/home/udg/git/EstChannel/mediciones/biurkoFrankaNlos/agc on/";


fid=fopen(path +"Fs38-Fr2170-bw28-wd10--1.dat",'rb');
imp2=fread(fid,'double');

%%%%%normalize
if 1==1
    imp = imp/ max(imp);
    imp2 = imp2/ max(imp2);
end


imp = imp(1:end);

t = 0:1/Fs:length(imp)/Fs -1/Fs;

figure
hold on
grid on
 stem(t,imp)
 stem(t,imp2)

hold off

%%%%%%% PDP
pdp = xcorr(imp,imp);
pdp = pdp((length(pdp)+1)/2:end);

figure
stem(pdp)


%%%%%%% noise calc


noise = pdp (100:250);

figure 
stem(noise)

promedio = mean (noise)
varianza = var(noise)
Thd= promedio +3*varianza

s = find(pdp > Thd); 
delays = (s-1)/Fs

 

figure 
stem(pdp(s))

tmean =sum (delays .* pdp(s))/sum(pdp(s));
tmeanNs=tmean/ 1e-9
trms = sqrt (  (sum(pdp(s) .*delays.^2) / sum(pdp(s)) ) - tmean^2 );
trmsNs = trms/1e-9

