function [offset] = offsetcalc(data,Fs)

format long

%%%%%%%%%%%%%%%%%%%%%%%

ot = 0.15;

sync = abs(data);
signal = sync(floor((ot+0.1)*Fs):floor((ot+0.12)*Fs));

figure
plot(signal)

noise = sync(floor((0.05)*Fs):floor((0.07)*Fs));

figure
plot(noise)

meanSignal = mean(signal);

meanNoise = mean(noise);
ratio = meanSignal/meanNoise;

threshold = meanNoise +0.2*ratio*meanNoise;
offset = floor(find(sync(0.05*Fs:end) > threshold,1) +0.4*Fs ) -30;

end

