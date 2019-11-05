Fs =38e6;
t  = 0:1/Fs:0.01-1/Fs;
s_i = 1* sin(2*pi*5e3*t);
s_q = zeros(1,length(s_i));

s = complex(s_i,s_q);

status = save_sc16q11("/dev/shm/testmatlab.bin",s)
