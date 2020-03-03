close all
clear all

N=10000;
Fs=10000;

noise = randn(1,N);

figure

subplot(2,1,1)
plot(noise)
title('Dominio de tiempo')
xlabel("Muestras [u.a.]");
ylabel("Amplitud [u.a.]");


Y = fftshift(noise);
fshift = (-N/2:N/2-1)*(Fs/N); % zero-centered frequency range
powershift = abs(Y).^2/N;     % zero-centered power



subplot(2,1,2)
plot(fshift,powershift)
title('Espectro frecuencial')
xlabel("Frecuencia [Hz]");
ylabel("Magnitud [u.a.]");