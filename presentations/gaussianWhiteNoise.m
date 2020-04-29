close all
clear all

N=10000;
Fs=10000*2*pi;

noise = randn(1,N);

figure

subplot(2,1,1)
plot(noise)
title('White Gaussian noise - Time domain')
xlabel("Samples [AU]");
ylabel("Magnitude [AU]");
ylim([-8 8])
%title('Dominio de tiempo')
%xlabel("Muestras [u.a.]");
%ylabel("Amplitud [u.a.]");

subplot(2,1,2)
n_fft = 2048; n_vec = 1000;
nt  = randn(n_vec,n_fft);
ntf = 1/sqrt(n_fft)*fft(nt,[],2);
ntf_pwr     = ntf.*conj(ntf);
ntf_pwr_avg = mean(ntf_pwr);
plot([-n_fft/2:n_fft/2-1]/n_fft,10*log10(fftshift(ntf_pwr_avg)));
axis([-0.5 0.5 -1 1]);
ylabel('Power spectral density [dB/Hz]');
xlabel('Norm. frequency [AU]');
title('White Gaussian noise - Power spectral density');
