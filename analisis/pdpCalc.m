function [pdp] = pdpCalc(h,Fs,plotMode)

pdp = abs(h).^2;
%pdp = xcorr(h,h);

%pdp = pdp((length(pdp)+1)/2:end);

pdp = pdp/max(pdp);

if plotMode ==1
    
    t = 0:1/Fs:length(pdp)/Fs - 1/Fs;
    t = t*1e9;
    figure
    stem(t,pdp)
end

end

