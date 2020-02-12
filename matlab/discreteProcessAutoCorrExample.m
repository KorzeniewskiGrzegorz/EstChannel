close all
clear all


t=-3:.1:3;

 for i=1:100
     y=randn(100,1); 
     rxx(:,:,i)=y*y';
 end

 
  figure
 surf(sum(rxx,3))
title("'continuos' channel")

filter=sinc(t);

figure
plot(filter)

 for i=1:100
     y=conv(filter,randn(100,1)); 
     ryy(:,:,i)=y*y';
 end
 
 
  figure
 surf(sum(ryy,3))
title(" discrete, sampled channel")
