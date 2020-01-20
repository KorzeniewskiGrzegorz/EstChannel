function [tmean,trms,tmax,b_50] = paramDelayNew(t,pdp,plotMode,noiseThreshold,i)
%t [ns]
format long

if nargin<5, i=1;  end  

l = length(pdp);
noise = pdp (floor(4*l/5):end);


promedio = mean (noise);
varianza = var(noise);
maks=max(noise);
Thd=noiseThreshold;

[delays , pdp_f  ]=noiseFilterWithThr(t,pdp,Thd );


if plotMode == 1
    figure

    stem(delays,pdp_f)
    title("pdp without noise n="+i)
end
    
    
tmean =sum (delays .* pdp_f)/sum(pdp_f);


trms = sqrt (  (sum(pdp_f .* (delays -tmean).^2) / sum(pdp_f) )  );


firstIdx = 1;
lastIdx = length(delays);
tmax= delays(lastIdx) - delays(firstIdx);

b_50 = 1/(5*trms*1e-9);
end

