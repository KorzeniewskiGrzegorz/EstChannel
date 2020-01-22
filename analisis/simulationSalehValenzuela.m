function [tSim,pdpSim , Lambda,lambda,Gamma,gamma] = simulationSalehValenzuela(pdp, Fs,clusterFirstIdx,clusterLastIdx,noiseThr)


t = 0:1/Fs:length(pdp)/Fs -1/Fs;
t=t*1e9; % [ns]

figure
grid on

stem(t,pdp)
title('PDP')
xlabel('delay[ns]'), ylabel('Magnitude') 
hold on

nClus = length(clusterFirstIdx);

%%%Avg cluster arrival time

deltaT= diff(clusterFirstIdx) / Fs * 1e9;

Lam = 1/mean(deltaT);

%%%Avg ray arrival time

[tRay , pdp_f]=noiseFilterWithThr(t,pdp,noiseThr);

deltaTRay = diff(tRay );

lam=1/mean(deltaTRay);

%%%% Cluster decay


b002=1; % amplitude of first cluster (in normalized case is always 1)



for i=1:nClus
    raysInClusterIdx{i} = clusterFirstIdx(i):clusterLastIdx(i);
end



x=t(clusterFirstIdx) -t( clusterFirstIdx(1) );
y= pdp(clusterFirstIdx);
Gam=minSqExp( x,y);% [ns]
clusterDecay = b002*exp(-t/Gam);

plot(t+(clusterFirstIdx(1)-1)/Fs*1e9,clusterDecay);


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

gam=minSqExp( x,y);% [ns]
 
for i=1:nClus
    
    idx = clusterFirstIdx(i);% first sample index
    b=pdp(idx); % first sample amplitude
    
    rayDecay = b*exp(-t/gam);

    plot(t+(idx-1)/Fs*1e9,rayDecay);
    
end    
 hold off
 
 

%%%%%%% PDP simulation Saleh Valenzuela
 
%MIMO-OFDM Wireless Communications with MATLAB��   Yong Soo Cho, Jaekwon Kim, Won Young Yang and Chung G. Kang 
%2010 John Wiley & Sons (Asia) Pte Ltd 
 
b002=1; % Power of 1st ray of 1st cluster  
N= 1; % Number of realizations
Lambda = Lam; % cluster arrival time
lambda=lam;  % ray arrival time
Gamma=Gam; % cluster decay
gamma=mean(gam); %ray decay
sigma_x=1; % Standard deviation of log-normal shadowing 
Nlos = 0; % 1 for Nlos, 0 for Los

[hsim,tSim,t0sim,npsim]= SV_model_ct(Lambda,lambda,Gamma,gamma,N,b002,sigma_x,Nlos);


    ryy= hsim*hsim';
    pdpSim = diag(ryy);
    pdpSim = pdpSim/max(pdpSim);
    
end