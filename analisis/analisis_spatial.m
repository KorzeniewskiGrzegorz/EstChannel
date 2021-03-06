close all
clear all

Fs = 38e6;
noiseThr = 0.01; %normalized threshold
plotMode = 0;
measurePoints=4;

distance(1)= 15; % tx-rx separation v1[m]
distance(2)= 20;
distance(3)= 28;
distance(4)= 36;

for j=1:measurePoints
    path = "/home/udg/git/EstChannel/mediciones/ed_mecanica_abierto/17-dec-19/Rx"+j+"/";

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
    %[pdp,piki(j,:)]=pdpCalc(hc,Fs,0,k,1,noiseThr,4);
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


figure
loglog(distance,trms,'blacko')
x1 = 12;
x2 = 40;

%title("RMS delay vs Tx-Rx separation ")
%xlabel("Tx-Rx separation [m]")
%ylabel("RMS delay [ns]")  

title("Retardo RMS vs distancia Tx-Rx")
xlabel("distancia Tx-Rx [m]")
ylabel("Retardo RMS [ns]")  

grid on
hold on

%model is y = a*x^b , curve fitting tool (cftool) used to estimate a and b
a= 20.12;
b=0.43;

tcurve = 12:40;

loglog(tcurve,a* (tcurve).^b,'r--')

%leg{1} = "Measured";
leg{1} = "Medido";
leg{2} = "p="+b;
legend(leg)
legend('Location','southeast')

axis([x1 x2 50 100])
hold off



%%% spatial PDP


%%%%%% data align to its max
for i=1:measurePoints
    [v, idx(i)] = max(pdpx(i,:));
end

preAlignIdx=6;
for i=1:measurePoints
   if idx(i)>preAlignIdx
       pdpx(i,:) = [pdpx(i,idx(i)-preAlignIdx+1:end) zeros(1,idx(i)-preAlignIdx)];
   else
       pdpx(i,:) = [zeros(1,preAlignIdx-idx(i)) pdpx(i,1:end-(preAlignIdx-idx(i)) )];
   end
end

%%% avg
sPDP = mean(pdpx);

sPDP = sPDP / max(sPDP);


[tmeanSp,trmsSp,tmaxSp,b_50Sp]=paramDelay(t, sPDP,plotMode,noiseThr);

%%% simulation Saleh Valenzuela

clusterFirstIdx = [6  8 14 18];
clusterLastIdx  = [7 12 17 20];
type = 0; % 0 for LoS, 1 for NLoS

[ tSim ,pdpSim, Lambda,lambda,Gamma,gamma,gam0,a] =  SalehValCalcFunc(sPDP,Fs,clusterFirstIdx,clusterLastIdx,type,noiseThr);

tSim = mean(tSim);
pdpSim=mean(pdpSim);
pdpSim = pdpSim/max(pdpSim);

[tmeanSim,trmsSim,tmaxSim,b_50Sim]=paramDelay(tSim, pdpSim,plotMode,noiseThr);


%%% results
figure
stem(t,sPDP,'black')

%title("Spatially-averaged PDP")
%xlabel('delay[ns]'), ylabel('Norm. magnitude [AU]') 

title("sPDP")
xlabel('Retardo [ns]'), ylabel('Magnitud norm. [u.a.]') 
grid on
axis([0 700 0 1])

figure
stem(t,sPDP,'black')

title("sPDP Estimado vs Simulado")
xlabel('Retardo [ns]'), ylabel('Magnitud norm. [u.a.]') 
grid on
hold on

%%% alignment of plots to its maxes
[v, dm] = max(sPDP);
[v, dsim] = max(pdpSim);

offsetM = (dm-1)/Fs*1e9 ; % ns
offsetS = tSim(dsim);
d = abs(dm-dsim);

offset = abs(offsetM-offsetS);
%%%

plot(tSim(1:100) + offset,pdpSim(1:100),'r--')
axis([0 700 0 1])

leg{1} = "Estimado";
leg{2} = "Simulado";
legend(leg)

hold off