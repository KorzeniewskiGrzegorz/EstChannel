close all
clear all

path = "/home/udg/git/EstChannel/mediciones/antena/";


fid=fopen(path +"antena_Fs35_Fr2170_bw20_wd10__0.dat",'rb');
imp=fread(fid,'double');



%%%%%normalize
if 1==2
    imp = imp/ max(imp);
end




figure
hold on
grid on
 stem(imp)


hold off

%%%%%%% PDP
pdp = xcorr(imp,imp);
pdp = pdp((length(pdp)+1)/2:end);

figure
plot(pdp)


