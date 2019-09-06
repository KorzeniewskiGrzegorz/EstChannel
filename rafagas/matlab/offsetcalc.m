function [offset] = offsetcalc(data,Fs)

format long

%%%%%%%%%%%%%%%%%%%%%%%


sync = abs(data);
signal = sync(floor((0.1+0.02)*Fs):floor((0.1+0.04)*Fs));

%figure
%plot(signal)

noise = sync(floor((0.1-0.04)*Fs):floor((0.1-0.02)*Fs));

%figure
%plot(noise)

meanSignal = mean(signal);

meanNoise = mean(noise);
ratio = meanSignal/meanNoise;

threshold = meanNoise +0.2*ratio*meanNoise;
offset = floor(find(sync > threshold,1) +0.1*Fs ) -30;

end

