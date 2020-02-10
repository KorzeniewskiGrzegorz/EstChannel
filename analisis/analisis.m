close all
clear all

Fs = 38e6;
noiseThr = 0.01; %normalized threshold
plotMode = 0 ;
%path="/home/udg/git/EstChannel/mediciones/ed_mecanica_abierto/17-dec-19/Rx1/";
path = "/home/udg/git/EstChannel/mediciones/quimica/7-02-2020/v4/";
load(path+'params.mat')

for i=1:k
    fid=fopen(path +"Fs38-Fr2300-bw28-wd10--"+i+"_i"+".dat",'rb');
    hreal(i,:)=fread(fid,'double');
    
    fid=fopen(path +"Fs38-Fr2300-bw28-wd10--"+i+"_q"+".dat",'rb');
    himag(i,:)=fread(fid,'double');
    
    hc(i,:)=abs(complex(hreal(i,:),himag(i,:)));
    
    figure
    stem(hc(i,:))
    title('h ')
    grid on
end




%%%%%%% PDP

pdp=pdpCalc(hc,Fs,1,k,1,noiseThr,4); 

%pdp = pdp/max(pdp);


t = 0:1/Fs:length(pdp)/Fs -1/Fs;
t= t*1e9;

figure
grid on

stem(t,pdp)
title('averaged PDP')

[tmean,trms,tmax,b_50]=paramDelay(t,pdp,plotMode,noiseThr);


tmean
trms 
tmax
b_50    