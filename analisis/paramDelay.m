function [tmeanNs,trmsNs,tmaxNs,b_50] = paramDelay(pdp,Fs)
format long

l = length(pdp);
noise = pdp (floor(2*l/5):end);


promedio = mean (noise);
varianza = var(noise);
Thd= 0.05;%(promedio +3*varianza);


s = find(pdp > Thd); 
delays = (s-1)/Fs;

 
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

