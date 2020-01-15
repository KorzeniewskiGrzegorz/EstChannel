close all
clear all

Fs = 38e6;
noiseThr = 0.01; %normalized threshold
path = "/home/udg/git/EstChannel/mediciones/ed_mecanica_abierto/17-dec-19/v4/";
k =5;

for i=1:k
    fid=fopen(path +"Fs38-Fr2300-bw28-wd10--"+i+"_i"+".dat",'rb');
    hreal(i,:)=fread(fid,'double');
    
    fid=fopen(path +"Fs38-Fr2300-bw28-wd10--"+i+"_q"+".dat",'rb');
    himag(i,:)=fread(fid,'double');
    
    hc(i,:)=abs(complex(hreal(i,:),himag(i,:)));
end


%%%%%%% PDP measured

pdp=pdpCalc(hc,Fs,0,k,1,noiseThr,1); 


t = 0:1/Fs:length(pdp)/Fs -1/Fs;
t=t*1e9;

figure
grid on

stem(t,pdp)
title('PDP')
xlabel('delay[ns]'), ylabel('Magnitude') 
hold on
%%%% Cluster decay

tLog = 0:1/Fs:length(pdp)/Fs -1/Fs;
tLog=tLog*1e9;
b002=1; % amplitude of first cluster (in normalized case is always 1)

Gam=60;% [ns]
ClusterDecay = b002*exp(-tLog/Gam);

plot(tLog+2/Fs*1e9,ClusterDecay);
%%%% Ray decay C#1

gam = 10;% [ns]
RayDecay = b002*exp(-tLog/gam);

plot(tLog+2/Fs*1e9,RayDecay);

%%%% Ray decay C#2
i = 5;% sample index
b=pdp(i); % sample amplitude
gam = 10;% [ns]
RayDecay = b*exp(-tLog/gam);

plot(tLog+(i-1)/Fs*1e9,RayDecay);

%%%% Ray decay C#3
i = 7; % sample index
b=pdp(i); % sample amplitude
gam = 25;% [ns]
RayDecay = b*exp(-tLog/gam);

plot(tLog+(i-1)/Fs*1e9,RayDecay);

%%%% Ray decay C#4
i = 10; % sample index
b=pdp(i); % sample amplitude
gam = 25; % [ns]
RayDecay = b*exp(-tLog/gam);

plot(tLog+(i-1)/Fs*1e9,RayDecay);


%%%%
hold off
 
 
%%%%%%% PDP simulated
 
%MIMO-OFDM Wireless Communications with MATLAB��   Yong Soo Cho, Jaekwon Kim, Won Young Yang and Chung G. Kang 
%2010 John Wiley & Sons (Asia) Pte Ltd 
 
b002=1; % Power of 1st ray of 1st cluster  
N=1 ; % Number of channels 
Lam=0.0233; lambda=2.5; 
Gam=60; gamma=10; 
sigma_x=3; % Standard deviation of log-normal shadowing 
Nlos = 0; % 1 for Nlos, 0 for Los

[hsim,tsim,t0sim,npsim]= SV_model_ct(Lam,lambda,Gam,gamma,N,b002,sigma_x,Nlos);
hsim=abs(hsim);

ryy= hsim*hsim';
pdpsim = diag(ryy);
pdpsim = pdpsim/max(pdpsim);

figure
stem(tsim,pdpsim,'ko');
title('Simulated PDP') 
xlabel('delay[ns]'), ylabel('Magnitude') 


