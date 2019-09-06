close all
clear all

path="/dev/shm/";
fid=fopen(path+"dataR.dat",'rb');

signalR=fread(fid,'float');
fid=fopen(path+"dataI.dat",'rb');
signalI=fread(fid,'float');

signal = signalI+signalR;
Fs=20e6;
threshold=0.003;
r=0.5;

figure
plot(signal)


data=signal((1-r)*Fs:(1+r)*Fs);

figure
plot(data)

worg=100000;
w=worg;

x=data;


v=floor(length(x)/w);


for i=1:v

     power(i) = (norm(x((i-1)*w+1:i*w))^2)/length(w);

end
    figure
    plot(-power)

    [value,os]  = max((-power));

    abspos=(os)*w + (1-r)*Fs

    x =signal(abspos:abspos+200000);
    figure
    plot(x)

    
    
    
for j=1:4
    lenA= length(x);
    w=w/10;
    v=floor(lenA/w);
    
    for i=1:v

     power(i) = (norm(x((i-1)*w+1:i*w))^2)/length(w);

    end
    der=diff(power);
    %figure
    %plot(der)
    
    [value,os] = findpeaks(der,'NPeaks',1,'MinPeakHeight',10/10^j );
    
 
    os-2

    abspos=abspos+(os-2)*w

    x =signal(abspos:abspos+w*100);
    %figure
    %plot(x)

    
end
    
%w=w/10000;
%lenA = length(x);
%v=floor(length(x)/w);

%for i=1:v-1

   % power(i) = (norm(x((i-1)*w+1:i*w))^2)/length(x((i-1)*w+1:i*w));
    
      

  
%end

%figure
%plot(-flip(power))
%[value,os]  = max(-power);

%abspos = abspos+os*w
%x =data(abspos:abspos+10000);
%figure
%plot(x)


