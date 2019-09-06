function [offset] = offsetcalc(signal,Fs,threshold,r)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here


data=signal((1-r)*Fs:(1+r)*Fs);

%figure
%plot(data)

a=[];

len=size(data);
len=len(1);

for i=1:len
  
   if data(i,1)<threshold
      a(end+1) =  i +(1-r)*Fs ;      
   end
end

%figure
%plot(a)


lenA=size(a);
lenA=lenA(2);

v=floor(lenA/10000);
der=diff(a);

%figure
%plot(der)




for i=1:v-1

    count =0;
    for j=1:9800
    
        if der(i*10000+j)== der(i*10000+j+1)
            count = count+1;
        end
        if count > 9500
           start = i*10000; 
        end
       
   end
   
   
end

[value,os] = findpeaks(der(start:start+20000),'NPeaks',1);


%figure
%plot(der(start:start+2000))

offset=Fs- a(start+os-value);


end

