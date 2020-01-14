function [pdp] = pdpCalc(h,Fs,plotMode,i)

h=h';
ryy= h*h';


 
%ERyy=sum(PA')/v; % Average the values 
%pdp= 
%ERyy = ERyy/ max(ERyy);

pdp = diag(ryy);

%pdp = pdp/max(pdp);

if plotMode ==1
    
    t = 0:1/Fs:length(pdp)/Fs - 1/Fs;
    t = t*1e9;
    figure
    stem(t,pdp)
    title("pdp n="'+i)
end

end

