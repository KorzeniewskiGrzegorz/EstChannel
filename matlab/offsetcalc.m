function [offset] = offsetcalc(data,Fs)

format long

%%%%%%%%%%%%%%%%%%%%%%%

ot = 0.15;

sync = real(data) + imag(data);
signal = sync(floor((ot+0.12)*Fs):floor((ot+0.14)*Fs));

%figure
%plot(signal)

noise = sync(floor((0.05)*Fs):floor((0.07)*Fs));

%figure
%plot(noise)

meanSignal = max(signal)

meanNoise = max(noise)

threshold = meanSignal - (meanSignal-meanNoise)*0.5


id1 = find(sync(0.05*Fs:end) > threshold,1) ;

id2 = find(sync(0.05*Fs:end) < -threshold,1) ;

id = [id1,id2]

offset = floor(min(id) +0.4*Fs  - (1/19e3)/8 * Fs);
end

