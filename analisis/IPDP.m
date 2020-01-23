close all
clear all 

%fi(m) = psi_m *delta(t − tm )

%ray power
%psi_m = (1/4) * (gamma^m)/(m^2)

%gamma - avg power reflection coef

%gamma = 1 - alfa

%alfa = suma ( S_u * alfa_u) / S

% alfa_u absorption coeff of the surface
%S total surface
% S_u surface area of _u

%ray delay tm

%tm = (tc/2)*(2m-1 )


%tc characteristic time of reverb of the building
%tc = (8V) / (cS)

%gamma = 0.12

Vd = 42*17.8*8.2;
Vu= 42*17.8/2 * (14-8.2);

V = Vd + Vu

S = 42*17.8 + (42*8.2)*2 + (17.8*8.2)*2 + ((14-8.2)*17.8/2 ) *2 + 2* ( sqrt((14-8.2)^2+(17.8/2)^2 ) * 42   )
c = 3e8;
tc= (8*V) / (c*S)

gamma = 0.50;
m = 1:20;
tm = (tc/2)*(2*m-1 );

for i=m 

    psi(i) = (1/4) * (gamma^i)/(i^2)
end

psi = psi/max(psi);
tm=tm*1e9;
figure
plot(tm,psi)