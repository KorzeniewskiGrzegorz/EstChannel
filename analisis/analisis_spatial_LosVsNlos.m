close all
clear all

Fs = 38e6;
noiseThr = 0.01; %normalized threshold
plotMode = 0;
%measurePoints=4;
measurePoints=5;

distance(1)= 5.5; % tx-rx separation v1[m]
distance(2)= 7;
distance(3)= 10;
distance(4)= 16;
distance(5)= 20;
for j=1:measurePoints
    %path = "/home/udg/git/EstChannel/mediciones/ed_mecanica_abierto/17-dec-19/Rx"+j+"/";
    path="/home/udg/git/EstChannel/mediciones/quimica/7-02-2020/v"+j+"/";
    load(path+'params.mat')

    for i=1:k
        fid=fopen(path +"Fs38-Fr2300-bw28-wd10--"+i+"_i"+".dat",'rb');
        hreal(i,:)=fread(fid,'double');

        fid=fopen(path +"Fs38-Fr2300-bw28-wd10--"+i+"_q"+".dat",'rb');
        himag(i,:)=fread(fid,'double');

        hc(i,:)=abs(complex(hreal(i,:),himag(i,:)));
    end


    %%%%%%% PDP
    [pdp]=pdpCalc(hc,Fs,0,k,1,noiseThr,4);
    pdp = pdp/max(pdp);
    pdpx(j,:) = pdp;
    


    t = 0:1/Fs:length(pdp)/Fs -1/Fs;
    t=t*1e9;
    
    figure
    stem(t,pdp,'black')
    title("PDP Rx"+j)
    %xlabel('delay[ns]'), ylabel('Norm. magnitude [AU]') 
    xlabel('Retardo [ns]'), ylabel('Magnitud norm. [u.a.]') 
    axis([0 700 0 1])
    grid on

    [tmean(j),trms(j),tmax(j),b_50(j)]=paramDelay(t, pdp,plotMode,noiseThr);

    
end


