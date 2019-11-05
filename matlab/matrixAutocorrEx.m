
close all
clear all
R=0.01; % pulse ratio (0-1 range) for signal break
duration=1;% signal duration [s]
wd=0.01; % window duration [s]
path="/dev/shm/";

Fs=10000; %Sampling Frequency
Fc=400; %Cut-off Frequency
 
w = Fc/(Fs/2); %Normalized frequency
%Design a low pass fitler with above mentioned specifications
[b,a]=butter(5,w,'low'); %5th order butterworth LPF


%%%%%%%%%


%Finding the Actual Impulse response of the LPF by applying a %generated impulse
N= Fs*wd ;
impulse=[1,zeros(1,N-1)]; %Defining an impulse
href=filter(b,a,impulse); %Apply the generated impulse at the filter's %input
 
figure;
subplot(3,1,1);
href = href/max(href); %normalized impulse response
plot(0:1/Fs*1000:N/Fs*1000-1/Fs*1000,href);

title('Actual impulse response');
xlabel('time [ms]')
grid;
 
%%%%%%%%%%%%%%%%%%%
% Sounding

IData = zeros(1,floor(Fs*duration));

v = duration/wd;



for i=1: v
    w = zeros(1,floor(Fs*wd));
    w(1,1:floor(Fs*wd)- floor(Fs*wd)*(1-R)) = randn(1,floor(Fs*wd)- floor(Fs*wd)*(1-R));


    IData(1,(i-1)*N+1:i*N) = w; 
end
IData = IData/ max(IData);
IData = IData';

channel = filter(b,a,IData);

%%%%%%%%%%%%%%%%%%%%%
% Estimation


y=zeros(N,v);

for i=0:v-1 % Run cross correlation for v times
    
    y=channel(i*N+1:i*N+N,1); % RX
    ryy= y*y';
    Ryy= ryy(:,1);
    
    
    
PA(:,i+1)=Ryy; %Store the results in an array
end
clear Ryx; 
 
ERyy=sum(PA')/v; % Average the values 

ERyy = ERyy/ max(ERyy);
h = ERyy;

subplot(3,1,2);
plot(0:1/Fs*1000:N/Fs*1000-1/Fs*1000,h);
title('Estimated Impulse Response');
xlabel('time [ms]')
grid;


%%%%%%%%%%%%%
Error = href - h;
subplot(3,1,3);
plot(0:1/Fs*1000:N/Fs*1000-1/Fs*1000,Error);
title('Estimation Error');
xlabel('time [ms]')
grid;
