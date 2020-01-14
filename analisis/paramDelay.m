function [tmeanNs,trmsNs,tmaxNs,b_50] = paramDelay(pdp,Fs,i,noiseThreshold)
format long

l = length(pdp);
noise = pdp (floor(4*l/5):end);


promedio = mean (noise);
varianza = var(noise);
maks=max(noise);
Thd=noiseThreshold;


s = find(pdp > Thd); 
delays = (s-1)/Fs;


    t = delays*1e9;
    figure
    
    stem(t,pdp(s))
    title("pdp without noise n="+i)
    
    
tmean =sum (delays .* pdp(s))/sum(pdp(s));
tmeanNs=tmean/ 1e-9;

trms = sqrt (  (sum(pdp(s) .* (delays -tmean).^2) / sum(pdp(s)) )  );
trmsNs = trms/1e-9;

firstIdx = 1;
lastIdx = length(delays);
tmax= delays(lastIdx) - delays(firstIdx);
tmaxNs = tmax/1e-9;
b_50 = 1/(5*trms);
end

