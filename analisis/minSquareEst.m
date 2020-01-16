function [est] = MinSq( x,y)

    %modelo y= exp(-x/Gam)  +r, r es ruido , vamos a estimar el parametro Gam
    % x,y,  datos observados

    N=1000;

    rango=0:1/N:100;
    U=zeros(1,length(rango));

    for j=1:length(rango) %un ciclo para probar el modelo para diferentes valores

        theta=exp(-x/rango(j));
        U(j)=sum((y-theta).^2);

    end

    figure
    plot(rango,U)
    xlabel("theta")
    ylabel("U(theta)")

    [value,ind] = min(U);
    est=rango(ind) % la solucion, el parametro estimado

    figure
    plot(x,y,x,exp(-x/est));

    

end

