close all
clear all

Fs = 38e6;
noiseThr = 0.01; %normalized threshold
path = "/home/udg/git/EstChannel/mediciones/ed_mecanica_abierto/17-dec-19/v1/";
k =4;

for i=1:k
    fid=fopen(path +"Fs38-Fr2300-bw28-wd10--"+i+"_i"+".dat",'rb');
    hreal(i,:)=fread(fid,'double');
    
    fid=fopen(path +"Fs38-Fr2300-bw28-wd10--"+i+"_q"+".dat",'rb');
    himag(i,:)=fread(fid,'double');
    
    hc(i,:)=abs(complex(hreal(i,:),himag(i,:)));
end


%%%%%%% PDP

pdp=pdpCalc(hc,Fs,1,k,1,noiseThr); 


t = 0:1/Fs:length(pdp)/Fs -1/Fs;

figure
grid on

stem(t,pdp)
title('PDP')

[tmean,trms,tmax,b_50]=paramDelay(pdp,Fs,1,noiseThr);

tmean
trms 
tmax
b_50    