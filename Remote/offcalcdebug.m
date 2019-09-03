
%UNTITLED2 Summary of this function goes here
%   DEBUG
close all
clear all
format long
path="/dev/shm/";
fid=fopen(path+"dataR.dat",'rb');
dataR=fread(fid,'float');

fid=fopen(path+"dataI.dat",'rb');
dataI=fread(fid,'float');
dataC=complex(dataR,dataI); 

signal=abs(dataC);

Fs=20e6;
threshold=0.0035;
r=0.5;
R=0.99;


data=signal((1-r)*Fs:(1+r)*Fs);

figure
plot(data)

a=[];

len=size(data);
len=len(1);

for i=1:len
  
   if data(i,1)<threshold
      a(end+1) =  i +(1-r)*Fs ;      
   end
end

figure
plot(a)


lenA=size(a);
lenA=lenA(2);

p=10000;

v=floor(lenA/p);
der=diff(a);

figure
plot(der)




for i=1:v-1

    count =0;
    for j=1:p*0.98
    
        if der(i*p+j)== der(i*p+j+1)
            count = count+1;
        end
        if count > p*0.95
           start = i*p; 
        end
       
   end
   
   
end

[value,os] = findpeaks(der(start:start+p*0.2),'NPeaks',1);


figure
plot(der(start:start+2000))

offset=(-1) *(Fs- a(start+os-value));

signalDuration = 1;
F=1/signalDuration ; 
calibrationOffset = signalDuration *Fs ; % conversion from time to samples


dataC=dataC(calibrationOffset+offset+1:calibrationOffset*2+offset-(Fs/F)*(1-R)+2);


lenD=size(dataC(:,1));
lenD=lenD(1,1);


%calibrated data plotting

figure

plot(0:1/Fs:lenD/Fs-1/Fs,abs(dataC))
title('Rx with offset')
xlabel('time [s]')
