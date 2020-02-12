

% white noise in pulses generator
function [ISync] = syncpulse(Fs,duration)

    R = 0.5;
    wd = duration - 0.1;
    
    ISync = zeros(1,floor(Fs*wd));
    
    t=0:1/Fs:wd*R;
    s1 = sin(2*pi*10e3*t);
    s2 = sin(2*pi*200*t);

    %s=1;

    
    ISync = [s1, s2, zeros(1,Fs*0.1)];
    




end

