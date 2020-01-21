close all
clear all

Fs = 38e6;
noiseThr = 0.01; %normalized threshold
plotMode = 0;
path = "/home/udg/git/EstChannel/mediciones/ed_mecanica_abierto/17-dec-19/Rx3/";
first= 0;

if first==1
    k =5; % # of measurements
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

pdp=pdpCalc(hc,Fs,plotMode,k,1,noiseThr,1); %calculates averagePDP in the same location


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
N= 1000; % Number of realizations
Lambda = Lam; % cluster arrival time
lambda=lam;  % ray arrival time
Gamma=Gam; % cluster decay
gamma=mean(gam); %ray decay
sigma_x=0; % Standard deviation of log-normal shadowing 
Nlos = 0; % 1 for Nlos, 0 for Los

[hsim,tsim,t0sim,npsim]= SV_model_ct(Lambda,lambda,Gamma,gamma,N,b002,sigma_x,Nlos);


for i=1:length(hsim)
    ryy= hsim(:,1)*hsim(:,1)';
    pdpsim = diag(ryy);
    pdpsim = pdpsim/max(pdpsim);
    
   [tmeanSim(i),trmsSim(i),tmaxSim(i),b_50Sim(i)]=paramDelay(tsim(:,i), pdpsim,plotMode,noiseThr); 
end


%%% Parameter comparison

 %measured
[tmean,trms,tmax,b_50]=paramDelay(t, pdp,plotMode,0.01);

 %simulated
tmeanSim = mean(tmeanSim);
trmsSim = mean(trmsSim);
tmaxSim = mean(tmaxSim);
b_50Sim = mean(b_50Sim);


%%% Plotting results

tsimPlot = tsim(:,length(tsim));

figure
stem(tsimPlot,pdpsim); % one realization of model
title('Simulated PDP') 
xlabel('delay[ns]'), ylabel('Norm. magnitude') 


figure
stem(t,pdp)
leg{1} = "measured";
hold on

%%% alignment of plots to its maxes
[v, dm] = max(pdp);
[v, dsim] = max(pdpsim);

offsetM = (dm-1)/Fs*1e9 ; % ns
offsetS = tsimPlot(dsim);
d = abs(dm-dsim);

offset = abs(offsetM-offsetS);
%%%

stem(tsimPlot +offset,pdpsim)
leg{2} = "simulated";
legend(leg)
title('Measured vs. Simulated ')
xlabel('delay[ns]'), ylabel('Norm. magnitude') 
hold off


