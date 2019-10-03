function [offset] = offsetcalc(data,Fs)
format long
%%%%%%%%%%%%%%%%%%%%%%%

s = real(data) + imag(data);
sync=s;%sync =doFilterLow(s);
figure
plot(0:1/Fs:length(sync)/Fs-1/Fs,sync)


zci = @(v) find(v(:).*circshift(v(:), [-1 0]) <= 0);                    % Returns Zero-Crossing Indices Of Argument Vector
zx = zci(sync);   

figure
plot(zx)

der=diff(zx);

figure
plot(der)

flips= flip(der);


threshold = max(flips(1:floor(length(flips)/10))) * 5 
idOdwrocone = find(flips > threshold,1) ;

id = length(zx) - idOdwrocone;

o = zx(id) + der(id);


offset = floor(o+ 0.1*Fs) 

%jedna czestotliwosc i bardzo duza, np 10 MHz cus takiego
%policzyc maksa ostatniego kawalka
% wszystko co jest mniejsze od polowy tego maksa wyzerowac
%odwrocic wektor
%pierwszy pik jest poszukiwany
%id piku length(zx)-1907277 <- znaleziony indeks z odwroconego wektoru
%oczekiwane id to 1109381 
% zx(1109381) + der(1109381) indeks ostatniej probki syncu
% dodac 0.1*Fs i mamy poczatek

end

