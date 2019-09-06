

% white noise in pulses generator
function [ISync] = syncpulse(Fs,duration)

    R = 0.5;
    wd = duration - 0.1;
    
    ISync = zeros(1,floor(Fs*wd));

    ISync(1,floor(Fs*wd)*R:end) = 5;
    
    ISync = [ISync, zeros(1,Fs*0.1)];
    




end

