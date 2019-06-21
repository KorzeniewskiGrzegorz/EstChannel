clear all
close all

load offsetprobki.mat

Fs=20e6;
threshold = 0.003;
r=0.05;



%[pks,locs] = findpeaks(probka((1-r)*Fs:(1+r)*Fs));

figure
plot(probka)

%locs=locs+(1-r)*Fs;
%data=[abs(pks),locs];

data=probka((1-r)*Fs:(1+r)*Fs);

figure
plot(data)

clear pks
clear locs

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

v=floor(lenA/1000);
der=diff(a);

figure
plot(der)




for i=1:v-1
    roznica=0;
    count =0;
    for j=1:980
    
        if der(i*1000+j)== der(i*1000+j+1)
            count = count+1;
        end
        if count > 950
           start = i*1000; 
        end
       
   end
   
   
end

[value,os] = findpeaks(der(start:start+2000),'NPeaks',1);
figure
plot(der(start:start+2000))

offset=Fs- a(start+os-2*value);