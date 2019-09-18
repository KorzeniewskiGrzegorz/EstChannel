

path = "/home/udg/git/EstChannel/mediciones/gps/";


fid=fopen(path +"Fs38-Fr2170-bw20-wd10--1.dat",'rb');
imp1=fread(fid,'double');

path = "/home/udg/git/EstChannel/mediciones/gps/";

fid=fopen(path +"Fs20-Fr2170-bw20-wd10--1.dat",'rb');
imp2=fread(fid,'double');

%%%%%normalize
if 1==1
    imp1 = imp1/ max(imp1);
    imp2 = imp2/ max(imp2);
end




figure
hold on
grid on
 plot(imp1)
% plot(imp2)

hold off

%%%%%%% PDP
pdp = xcorr(imp,imp);
pdp = pdp((length(pdp)+1)/2:end);

figure
stem(pdp)


