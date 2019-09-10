close all
clear all

fid=fopen("shiftedCompleto.dat",'rb');
completo=fread(fid,'double');

fid=fopen("shiftedRaf0_5.dat",'rb');
raf0_5=fread(fid,'double');

fid=fopen("shiftedRaf0_1.dat",'rb');
raf0_1=fread(fid,'double');

fid=fopen("shiftedRaf0_01.dat",'rb');
raf0_01=fread(fid,'double');

fid=fopen("shiftedRaf0_001.dat",'rb');
raf0_001=fread(fid,'double');

%load('completo.mat')
%load('raf0_5.mat')
%load('raf0_1.mat')
%load('raf0_01.mat')
%load('raf0_001.mat')

%f = fopen ("shiftedcompleto.dat", 'wb');
%v = fwrite (f, completo,'double');
%fclose (f);

%f = fopen ("raf0_5.dat", 'wb');
%v = fwrite (f, raf0_5,'double');
%fclose (f);

%f = fopen ("raf0_1.dat", 'wb');
%v = fwrite (f, raf0_1,'double');
%fclose (f);

%f = fopen ("raf0_01.dat", 'wb');
%v = fwrite (f, raf0_01,'double');
%fclose (f);

%f = fopen ("raf0_001.dat", 'wb');
%v = fwrite (f, raf0_001,'double');
%fclose (f);


%%%%%normalize

completo = completo / max(completo);
raf0_5 = raf0_5 / max(raf0_5);
raf0_1 = raf0_1/ max(raf0_1);
raf0_01 = raf0_01/ max(raf0_01);
raf0_001 = raf0_001/ max(raf0_001);




figure
hold on
grid on
hplot1 = plot((completo), 'DisplayName', '1.0');
hplot2 = plot((raf0_5), 'DisplayName', '0.5');
hplot3 = plot((raf0_1), 'DisplayName', '0.1');
hplot4 = plot((raf0_01), 'DisplayName', '0.01');
hplot5 = plot((raf0_001), 'DisplayName', '0.001');

hold off

legend([hplot1, hplot2,hplot3, hplot4,hplot5]);