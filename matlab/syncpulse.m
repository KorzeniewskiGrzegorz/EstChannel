

% white noise in pulses generator
function [ISync] = syncpulse(Fs,R,duration,wd)


    ISync = zeros(1,floor(Fs*duration));

    v = duration/wd;
    N= Fs*wd ;

    i=2;
    w = zeros(1,floor(Fs*wd));
    w(1,1:floor(Fs*wd)- floor(Fs*wd)*(1-R)) = 5;

    ISync(1,(i-1)*N+1:i*N) = w; 




end

