function [est] = minSqExp( x,y)

    %modelo y=b* exp(-x/Gam)  +r, r es ruido , vamos a estimar el parametro Gam
    % x,y,  datos observados

    N=1000;

    rango=0:1/N:200;
    U=zeros(1,length(rango));

    b=y(1);
    for j=1:length(rango) %un ciclo para probar el modelo para diferentes valores

        theta=b*exp(-x/rango(j));
        U(j)=sum((y-theta).^2);

    end

    %figure
    %plot(x,y);
    
    %figure
    %plot(rango,U)
    %xlabel("theta")
   % ylabel("U(theta)")

    [value,ind] = min(U);
    est=rango(ind); % la solucion, el parametro estimado

    %figure
    %stem(x,y)
   
    %hold on
   % plot(x,b*exp(-x/60));
    %hold off

end

