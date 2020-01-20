close all
clear all

Fs = 38e6;
noiseThr = 0.01; %normalized threshold
plotMode = 0;

measurePoints=4;

distance(1)= 36; % tx-rx separation v1[m]
distance(2)= 28;
distance(3)= 20;
distance(4)= 15;

for j=1:measurePoints
    path = "/home/udg/git/EstChannel/mediciones/ed_mecanica_abierto/17-dec-19/v"+j+"/";
    load(path+'params.mat')

    for i=1:k
        fid=fopen(path +"Fs38-Fr2300-bw28-wd10--"+i+"_i"+".dat",'rb');
        hreal(i,:)=fread(fid,'double');

        fid=fopen(path +"Fs38-Fr2300-bw28-wd10--"+i+"_q"+".dat",'rb');
        himag(i,:)=fread(fid,'double');

        hc(i,:)=abs(complex(hreal(i,:),himag(i,:)));
    end


    %%%%%%% PDP

    pdp=pdpCalc(hc,Fs,0,k,1,noiseThr,4); 


    t = 0:1/Fs:length(pdp)/Fs -1/Fs;

    figure
    grid on

    stem(t,pdp)
    title("PDP v"+j)

    [tmean(j),trms(j),tmax(j),b_50(j)]=paramDelay(t, pdp,plotMode,noiseThr);

    
end


figure

stem(distance,trms)
title("RMS delay vs Tx-Rx separation ")
xlabel("Tx-Rx separation [m]")
ylabel("RMS delay [ns]")    

