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
Vu= 42*(17.8/2) * (12-8.2);

V = Vd + Vu

S = 42*17.8 + (42*8.2)*2 + (17.8*8.2)*2 + ((12-8.2)*(17.8/2) ) *2 + 2* ( sqrt((12-8.2)^2+(17.8/2)^2 ) * 42   )
c = 3e8;
tc= (8*V) / (c*S)

gamma = 0.9;
m = 1:20;
tm = (tc/2)*(2*m-1 );
tm= [0 tm ];
psi(1)=1;

for i=m 

    psi(i+1) = (1/4) * (gamma^i)/(i^2);
end

%psi = psi/max(psi);
tm=tm*1e9;

%x=[78.9473684210526,    131.578947368421,    289.473684210526,   394.736842105263,  700];
%y=[               1,   0.401143217263205,  0.0573353288367250, 0.0311203740186049,    0];

x=[52.6315789473684,    105.263157894737,    157.894736842105,    236.842105263158,  600];
y=[               1,   0.353713466132422,   0.125261475734880,  0.0740759502853946,    0];

figure
plot(x,y)
grid on
hold on

offset = x(1)-tm(1);


plot(tm+offset,psi)

hold off

