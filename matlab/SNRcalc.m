function [snr] = SNRcalc(data,Fs, id)
format long
%%%%%%%%%%%%%%%%%%%%%%%

data = real(data) + imag(data);



signal = data( length(data)-0.05*Fs:end);

noise = data(id +0.04*Fs: id +0.06*Fs);

avgSigPwr = mean(signal.^2)
avgNsPwr = mean(noise.^2)

snr = 10*log10(avgSigPwr/avgNsPwr)

end

