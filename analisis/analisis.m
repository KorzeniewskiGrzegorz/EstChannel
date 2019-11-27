close all
clear all

path = "/home/udg/git/EstChannel/mediciones/testZapisu/";
%path = "/home/udg/git/EstChannel/mediciones/biurkoFrankaNlos/agc off/";
Fs = 38e6;

k =1;
i=1;
%for i=1:k
    fid=fopen(path +"Fs38-Fr2300-bw28-wd10--2_i"+".dat",'rb');
    hreal(i,:)=fread(fid,'double');
    
    fid=fopen(path +"Fs38-Fr2300-bw28-wd10--2_q"+".dat",'rb');
    himag(i,:)=fread(fid,'double');
%end

h(i,:)=abs(complex(hreal(i,:),himag(i,:)));



for i=1:k
    h(i,:) = h(i,:)/max(h(i,:)) ;
    [v, idx(i)] = max(h(i,:));

end


%idxref = 5;
%if 1==1
%    for i=1:k
%       h(i,:) =circshift(h(i,:),idxref-idx(i));
%    end
%end


t = 0:1/Fs:length(h(1,:))/Fs -1/Fs;
leg=cell(1,k);

figure
hold on
grid on
for i=1:k
        stem(t,h(i,:)) 
        leg{i} = sprintf('n = %i',i);
end
hold off

legend(leg)
%%%%%%% PDP
for i=1:k
       pdp(i,:)=pdpCalc(h(i,:),Fs,1); 
end

%%%%%%%%
for i=1:k
      [tmeanp(i),trmsp(i),tmaxp(i),b_50p(i)]=paramDelay(pdp(i,:),Fs); 
end

tmeanNs = mean(tmeanp)
trmsNs  = mean(trmsp)
tmaxNs  = mean(tmaxp)
b_50    = mean(b_50p)


N=length(h(1,:));
X=fftshift(fft(h(1,:)));
figure;
plot(Fs*(-N/2:N/2-1)/N,abs(X));
grid on;
