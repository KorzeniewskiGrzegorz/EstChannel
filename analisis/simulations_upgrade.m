close all
clear all

Fs = 38e6;
noiseThr = 0.01; %normalized threshold
path = "/home/udg/git/EstChannel/mediciones/ed_mecanica_abierto/17-dec-19/Rx4/";
first=0;

if first==1
    k =5; % # of measurements
    clusterFirstIdx = [3 5 8  12 15];
    clusterLastIdx  = [4 7 10 14 20];
else
    load(path+'params.mat')
end

for i=1:k
    fid=fopen(path +"Fs38-Fr2300-bw28-wd10--"+i+"_i"+".dat",'rb');
    hreal(i,:)=fread(fid,'double');
    
    fid=fopen(path +"Fs38-Fr2300-bw28-wd10--"+i+"_q"+".dat",'rb');
    himag(i,:)=fread(fid,'double');
    
    hc(i,:)=abs(complex(hreal(i,:),himag(i,:)));
end


%%%%%%% PDP measured

pdp=pdpCalc(hc,Fs,0,k,1,noiseThr,1); %calculates averagePDP in the same location


t = 0:1/Fs:length(pdp)/Fs -1/Fs;
t=t*1e9;

figure
grid on

stem(t,pdp)
title('PDP')
xlabel('delay[ns]'), ylabel('Magnitude') 
hold on

%%%Avg cluster arrival time

deltaT= diff(clusterFirstIdx) / Fs * 1e9;

Lam = 1/mean(deltaT);

%%%Avg ray arrival time

[tRay , pdp_f]=noiseFilterWithThr(t,pdp,noiseThr);

deltaTRay = diff(tRay );

lam=1/mean(deltaTRay);


%%%% Cluster decay


b002=1; % amplitude of first cluster (in normalized case is always 1)
nClus = length(clusterFirstIdx);


for i=1:nClus
    raysInClusterIdx{i} = clusterFirstIdx(i):clusterLastIdx(i);
end



x=t(clusterFirstIdx) -t( clusterFirstIdx(1) );
y= pdp(clusterFirstIdx);
Gam=minSqExp( x,y);% [ns]
clusterDecay = b002*exp(-t/Gam);

plot(t+(clusterFirstIdx(1)-1)/Fs*1e9,clusterDecay);

%Ray decays


for i=1:nClus
    
    idx = clusterFirstIdx(i);% first sample index
    b=pdp(idx); % sample amplitude
    raysIdxs=cell2mat(raysInClusterIdx(i));
    
    x= t( raysIdxs ) -t( idx );
    y= pdp(raysIdxs);
    
    gam(i)=minSqExp( x,y);% [ns]
    rayDecay = b*exp(-t/gam(i));

    plot(t+(idx-1)/Fs*1e9,rayDecay);
    
    
end

hold off
 
 
%%%%%% gamma function
x=t(clusterFirstIdx);
p=polyfit(x, gam,1); % [ns]
a = p(1);
gam0 = p(2);

%%%%%%% PDP simulated
 
%MIMO-OFDM Wireless Communications with MATLAB��   Yong Soo Cho, Jaekwon Kim, Won Young Yang and Chung G. Kang 
%2010 John Wiley & Sons (Asia) Pte Ltd 
 
b002=1; % Power of 1st ray of 1st cluster  
N=1 ; % Number of channels 
Lambda = Lam; % cluster arrival time
lambda=lam;  % ray arrival time
Gamma=Gam; % cluster decay 
sigma_x=1; % Standard deviation of log-normal shadowing 
Nlos = 0; % 1 for Nlos, 0 for Los

[hsim,tsim,t0sim,npsim]= SVUPGR_model(Lam,lambda,Gamma,gam0,a,N,b002,sigma_x,Nlos);

hsim=abs(hsim);

ryy= hsim*hsim';
pdpsim = diag(ryy);
pdpsim = pdpsim/max(pdpsim);

figure
stem(tsim,pdpsim,'ko');
title('Simulated PDP') 
xlabel('delay[ns]'), ylabel('Magnitude') 


