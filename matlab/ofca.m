close all
clear all 

path="/dev/shm/";
format long
load("sync.mat")
fid=fopen(path+"ruidoR.dat",'rb');
ruidoR=fread(fid,'float');

fid=fopen(path+"ruidoI.dat",'rb');
ruidoI=fread(fid,'float');
Fs =38e6

ruidoR = ruidoR(1:0.6*Fs);
ruidoI = ruidoI(1:0.6*Fs);


ruido=ruidoR + ruidoI; 
clear ruidoR
clear ruidoI
%%%%%%%%%%%%%%%%%%%%%%%


data = y;

sync = real(data) + imag(data);

%figure
%plot(0:1/Fs:length(sync)/Fs-1/Fs,sync)

%filt = decimate(sync,30);


%Transformada de Hilbert
    ch1=hilbert(ruido);
    ch2=hilbert(sync);
    
    anguloTx=angle(ch1);
    anguloRx=angle(ch2);
    
    t = 0:1/Fs:(0.6 - 1/Fs);
    
    figure
    plot(t,anguloTx)
    
    figure
    plot(t,anguloRx)


%zci = @(v) find(v(:).*circshift(v(:), [-1 0]) <= 0);                    % Returns Zero-Crossing Indices Of Argument Vector
%zx = zci(sync);   

%figure
%plot(zx)

%der=diff(zx);

%figure
%plot(der)

%flips= flip(der);

%threshold = 100;
%idOdwrocone = find(flips > threshold,1) ;

%id = length(zx) - idOdwrocone;

%offset = zx(id) + der(id)

%jedna czestotliwosc i bardzo duza, np 10 MHz cus takiego
%policzyc maksa ostatniego kawalka
% wszystko co jest mniejsze od polowy tego maksa wyzerowac
%odwrocic wektor
%pierwszy pik jest poszukiwany
%id piku length(zx)-1907277 <- znaleziony indeks z odwroconego wektoru
%oczekiwane id to 1109381 
% zx(1109381) + der(1109381) indeks ostatniej probki syncu
% dodac 0.1*Fs i mamy poczatek

