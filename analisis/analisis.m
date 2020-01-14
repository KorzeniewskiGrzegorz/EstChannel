close all
clear all

path = "/home/udg/git/EstChannel/mediciones/ed_mecanica_abierto/17-dec-19/v1/";
Fs = 38e6;

k =4;
i=1;
for i=1:k
    fid=fopen(path +"Fs38-Fr2300-bw28-wd10--"+i+"_i"+".dat",'rb');
    hreal(i,:)=fread(fid,'double');
    
    fid=fopen(path +"Fs38-Fr2300-bw28-wd10--"+i+"_q"+".dat",'rb');
    himag(i,:)=fread(fid,'double');
    
    hc(i,:)=abs(complex(hreal(i,:),himag(i,:)));
end





for i=1:k
    hc(i,:) = hc(i,:)/max(hc(i,:)) ;
    [v, idx(i)] = max(hc(i,:));

end


idxref = 10;
if 1==1
   for i=1:k
       if idx(i)>idxref
           hc(i,:) = [hc(i,idx(i)-idxref+1:end) zeros(1,idx(i)-idxref)];
       else
           hc(i,:) = [zeros(1,idxref-idx(i)) hc(i,1:end-(idxref-idx(i)) )];
       end
   end
end

for i=1:k
  
   h(i,:) = hc(i,1:50);
   
end


t = 0:1/Fs:length(h(1,:))/Fs -1/Fs;
leg=cell(1,k);

figure
hold on
grid on
for i=1:k
        stem(t,h(i,:))
        title('impulse response h(t)')
        leg{i} = sprintf('n = %i',i);
end
hold off

legend(leg)
%%%%%%% PDP
for i=1:k
       pdp(i,:)=pdpCalc(h(i,:),Fs,1,i); 
end

%%%%%%%%
for i=1:k
     [tmeanp(i),trmsp(i),tmaxp(i),b_50p(i)]=paramDelay(pdp(i,:),Fs,i); 
end

tmeanNs = mean(tmeanp)
trmsNs  = mean(trmsp)
tmaxNs  = mean(tmaxp)
b_50    = mean(b_50p)


%N=length(h(1,:));
%X=fftshift(fft(h(1,:)));
%figure;
%plot(Fs*(-N/2:N/2-1)/N,abs(X));
%grid on;
