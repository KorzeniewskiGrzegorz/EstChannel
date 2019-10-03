function [tmeanNs,trmsNs] = paramDelay(pdp,Fs)
format long

l = length(pdp);
noise = pdp (floor(4*l/5):end);


promedio = mean (noise);
varianza = var(noise);
Thd= promedio +3*varianza;


s = find(pdp > Thd); 
delays = (s-1)/Fs;

 
tmean =sum (delays .* pdp(s))/sum(pdp(s));
tmeanNs=tmean/ 1e-9;

trms = sqrt (  (sum(pdp(s) .* (delays -tmean).^2) / sum(pdp(s)) )  );
trmsNs = trms/1e-9;

end

