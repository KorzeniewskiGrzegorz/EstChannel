close all
clear all

Fs = 38e6;
noiseThr = 0.01; %normalized threshold
path = "/home/udg/git/EstChannel/mediciones/ed_mecanica_abierto/17-dec-19/v3/";
first= 1;

if first==1
    k =1; % # of measurements
    clusterFirstIdx = [4  6 12 15 19];
    clusterLastIdx  = [5 11 13 17 21];
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
%%%% Cluster decay


b002=1; % amplitude of first cluster (in normalized case is always 1)
nClus = length(clusterFirstIdx);


for i=1:nClus
    raysInClusterIdx{i} = clusterFirstIdx(i):clusterLastIdx(i);
end



x=t(clusterFirstIdx) -t( clusterFirstIdx(1) );
y= pdp(clusterFirstIdx);
Gam=minSq( x,y);% [ns]
clusterDecay = b002*exp(-t/Gam);

plot(t+(clusterFirstIdx(1)-1)/Fs*1e9,clusterDecay);

 hold on
%Ray decays

x=[];
y=[];
for i=1:nClus
    
    idx = clusterFirstIdx(i);% first sample index
    b=pdp(idx); % first sample amplitude
    raysIdxs=cell2mat(raysInClusterIdx(i));
    
    x=[x (t( raysIdxs ) -t( idx ) )];
    y=[y (pdp(raysIdxs)/b)];
    
    
    
end

%data sort
c= [x;y];
c =sortrows(c').';
x=c(1,:);
y=c(2,:);

gam=minSq( x,y);% [ns]
 
for i=1:nClus
    
    idx = clusterFirstIdx(i);% first sample index
    b=pdp(idx); % first sample amplitude
    
    rayDecay = b*exp(-t/gam);

    plot(t+(idx-1)/Fs*1e9,rayDecay);
    
end    
 hold off
%%%%%%% PDP simulated
 
%MIMO-OFDM Wireless Communications with MATLAB��   Yong Soo Cho, Jaekwon Kim, Won Young Yang and Chung G. Kang 
%2010 John Wiley & Sons (Asia) Pte Ltd 
 
b002=1; % Power of 1st ray of 1st cluster  
N=1 ; % Number of channels 
Lam=0.0233; lambda=2.5; 
Gamma=Gam; gamma=mean(gam); 
sigma_x=3; % Standard deviation of log-normal shadowing 
Nlos = 0; % 1 for Nlos, 0 for Los

[hsim,tsim,t0sim,npsim]= SV_model_ct(Lam,lambda,Gamma,gamma,N,b002,sigma_x,Nlos);
hsim=abs(hsim);

ryy= hsim*hsim';
pdpsim = diag(ryy);
pdpsim = pdpsim/max(pdpsim);

figure
stem(tsim,pdpsim,'ko');
title('Simulated PDP') 
xlabel('delay[ns]'), ylabel('Magnitude') 


