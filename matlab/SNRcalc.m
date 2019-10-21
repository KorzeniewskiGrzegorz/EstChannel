function [snr] = SNRcalc(data,Fs, id)
format long
%%%%%%%%%%%%%%%%%%%%%%%

data = real(data) + imag(data);



signal = data( id-0.15*Fs:id-0.13*Fs);

noise = data(id -0.06*Fs: id -0.04*Fs);
figure
plot(signal)

figure
plot(noise)


avgSigPwr = mean(signal.^2)
avgNsPwr = mean(noise.^2)

snr = 10*log10(avgSigPwr/avgNsPwr)

end

