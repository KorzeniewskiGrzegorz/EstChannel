

% white noise in pulses generator
function [ISync] = syncpulse(Fs,duration)

    R = 0.5;
    wd = duration - 0.1;
    
    ISync = zeros(1,floor(Fs*wd));
    
    t=0:1/Fs:wd*R;
    s = sin(2*pi*19e3*t);
    figure
    plot(s)
    %s=1;
    ISync(1,floor(Fs*wd)*R:end) = s;
    
    ISync = [ISync, zeros(1,Fs*0.1)];
    




end

