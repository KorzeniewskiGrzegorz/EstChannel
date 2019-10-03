%close all
clear all

path = "/home/udg/git/EstChannel/mediciones/biurkoFranka/agc off/";

Fs = 38e6;

k =1;

for i=1:k
    fid=fopen(path +"Fs38-Fr2170-bw28-wd10--"+i+".dat",'rb');
    h(i,:)=fread(fid,'double');
end

%%%%%normalize
if 1==1
    for i=1:k
        %h(i,:) = h(i,:)/max(h(i,:)) ;
        [v, idx(i)] = max(h(i,:));

    end
end

idxref = 5
if 1==1
    for i=1:k
        h(i,:) =circshift(h(i,:),idxref-idx(i));
    end
end


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
      [tmean(i),trms(i)]=paramDelay(pdp(i,:),Fs); 
end

tm = mean(tmean)
tr = mean(trms)

