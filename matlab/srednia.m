dataC = 0:100;

eRyy=0;
for i=0:100 %calculate autocorrelation matrix for v times
    
    y=dataC(i+1); % RX
    ryy= y;
    if(i>0)
        eRyy = ((i)*eRyy + ryy)/(i+1)
    end
end

sr = sum(dataC)/101