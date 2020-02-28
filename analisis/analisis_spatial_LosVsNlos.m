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


%%% LoS spatial avg

a_pdpLos(1,:) = pdpx(1,:);
a_pdpLos(2,:) = pdpx(3,:);

sPDPLoS = mean(a_pdpLos);

figure
stem(t,sPDPLoS,'black')
title("sPDP LoS")
xlabel('Retardo [ns]'), ylabel('Magnitud norm. [u.a.]') 
axis([0 700 0 1])
grid on

[tmeanLos,trmsLos,tmaxLos,b_50Los]=paramDelay(t, sPDPLoS,plotMode,noiseThr);

%%% NLoS spatial avg

a_pdpNLos(1,:) = pdpx(2,:);
a_pdpNLos(2,:) = pdpx(4,:);
a_pdpNLos(3,:) = pdpx(5,:);

sPDPNLoS = mean(a_pdpNLos);

figure
stem(t,sPDPNLoS,'black')
title("sPDP NLoS")
xlabel('Retardo [ns]'), ylabel('Magnitud norm. [u.a.]') 
axis([0 700 0 1])
grid on

[tmeanNLos,trmsNLos,tmaxNLos,b_50NLos]=paramDelay(t, sPDPNLoS,plotMode,noiseThr);


%%%%%%%% Simulations

%%% LoS

clusterFirstIdx = [6  9 13 15];
clusterLastIdx  = [8 12 14 17];
type = 0; %% 0 for LoS
[ tSimLos ,pdpSimLos, LambdaLos,lambdaLos,GammaLos,gammaLos,gam0Los,aLos] =  SalehValCalcFunc(sPDPLoS,Fs,clusterFirstIdx,clusterLastIdx,type,noiseThr);

tSimLos = mean(tSimLos);
pdpSimLos=mean(pdpSimLos);
pdpSimLos = pdpSimLos/max(pdpSimLos);

[tmeanSimLos,trmsSimLos,tmaxSimLos,b_50SimLos]=paramDelay(tSimLos, pdpSimLos,plotMode,noiseThr);

figure
stem(t,sPDPLoS,'black')

title("sPDP LoS Estimado vs Simulado")
xlabel('Retardo [ns]'), ylabel('Magnitud norm. [u.a.]') 
grid on
hold on

%%% alignment of plots to its maxes
[v, dm] = max(sPDPLoS);
[v, dsim] = max(pdpSimLos);

offsetM = (dm-1)/Fs*1e9 ; % ns
offsetS = tSimLos(dsim);
d = abs(dm-dsim);

offset = abs(offsetM-offsetS);
%%%

plot(tSimLos(1:100) + offset,pdpSimLos(1:100),'r--')
axis([0 700 0 1])

leg{1} = "Estimado";
leg{2} = "Simulado";
legend(leg)

hold off


%%% NLoS

clusterFirstIdx = [6 7 10 13];
clusterLastIdx  = [7 9 12 16];
type = 1; %% 0 for LoS
[ tSimNLos ,pdpSimNLos, LambdaNLos,lambdaNLos,GammaNLos,gammaNLos,gam0NLos,aNLos] =  SalehValCalcFunc(sPDPNLoS,Fs,clusterFirstIdx,clusterLastIdx,type,noiseThr);

tSimNLos = nanmean(tSimNLos);
pdpSimNLos = nanmean(pdpSimNLos);

pdpSimNLos = pdpSimNLos/max(pdpSimNLos);

[tmeanSimNLos,trmsSimNLos,tmaxSimNLos,b_50SimNLos]=paramDelay(tSimNLos, pdpSimNLos,plotMode,noiseThr);

figure
stem(t,sPDPNLoS,'black')

title("sPDP NLoS Estimado vs Simulado")
xlabel('Retardo [ns]'), ylabel('Magnitud norm. [u.a.]') 
grid on
hold on

%%% alignment of plots to its maxes
[v, dm] = max(sPDPNLoS);
[v, dsim] = max(pdpSimNLos);

offsetM = (dm-1)/Fs*1e9 ; % ns
offsetS = tSimNLos(dsim);
d = abs(dm-dsim);

offset = abs(offsetM-offsetS);
%%%

plot(tSimNLos(1:100) + offset,pdpSimNLos(1:100),'r--')
axis([0 700 0 1])

leg{1} = "Estimado";
leg{2} = "Simulado";
legend(leg)

hold off


